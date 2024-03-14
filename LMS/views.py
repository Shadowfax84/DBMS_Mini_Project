from .models import Attendance
from django.shortcuts import render, get_object_or_404, redirect
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from datetime import datetime
from django.contrib import messages
import matplotlib
from .forms import MarksForm
matplotlib.use('Agg')


def landing_page(request):
    return render(request, 'landing.html')


def home(request):
    return render(request, 'home.html')


def student_signup(request):
    departments = Dept.objects.all()
    courses = Course.objects.all()
    if request.method == 'POST':
        usn = request.POST.get('usn')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        joining_year = request.POST.get('joining_year')
        dept_id = request.POST.get('dept_id')
        subjects = request.POST.getlist('subjects')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('/student-signup/')  # Redirect to signup page

         # Retrieve the Dept instance corresponding to the dept_id
        try:
            dept_instance = Dept.objects.get(Dept_ID=dept_id)
        except Dept.DoesNotExist:
            messages.error(request, 'Invalid Department ID.')
            return redirect('/student-signup/')  # Redirect to signup page

        student = Student.objects.create(
            USN=usn,
            Name=name,
            Gender=gender,
            Phone_No=phone_no,
            Email=email,
            Joining_Year=joining_year,
            Dept_ID=dept_instance,
        )
        # Add selected subjects to the student
        student.Subject_ID.set(subjects)
        # Create a new user account
        user = User.objects.create_user(
            username=usn, password=password, email=email)

        if user:
            return redirect('/login-page/')

    return render(request, 'student_signup.html', {'departments': departments, 'courses': courses})


def teacher_signup(request):
    departments = Dept.objects.all()
    courses = Course.objects.all()

    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        name = request.POST.get('name')
        qualifications = request.POST.get('Qualifications')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        papers_published = request.POST.get('papers_published')
        dept_id = request.POST.get('dept_id')
        subjects = request.POST.getlist('subjects')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('/teacher-signup/')  # Redirect to signup page

        # Retrieve the Dept instance corresponding to the dept_id
        try:
            dept_instance = Dept.objects.get(Dept_ID=dept_id)
        except Dept.DoesNotExist:
            messages.error(request, 'Invalid Department ID.')
            return redirect('/teacher-signup/')  # Redirect to signup page

        # Create a new faculty instance
        faculty = Faculty.objects.create(
            Faculty_ID=faculty_id,
            Name=name,
            Qualifications=qualifications,
            Papers_Published=papers_published,
            Phone_No=phone_no,
            Email=email,
        )
        # Add selected subjects to the faculty
        faculty.Subject_ID.set(subjects)
        # Add department to the faculty
        faculty.Dept_ID.add(dept_instance)

        # Create a new user account
        user = User.objects.create_user(
            username=faculty_id, password=password, email=email)

        if user:
            return redirect('/login-page/')

    return render(request, 'teacher_signup.html', {'departments': departments, 'courses': courses})


def login_page(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'student':
            return redirect('student_login')
        elif role == 'teacher':
            return redirect('teacher_login')
        elif role == 'admin':
            return redirect('/admin/')
    return render(request, 'login_page.html')


def student_login(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        password = request.POST.get('password')
        print(usn, password)

        # Authenticate the user
        user = authenticate(request, username=usn, password=password)
        print("good")
        if user is not None:
            print("ifin")
            login(request, user)
            print("loggedin")
            # Create a new LoginHistory record for the logged-in user
            LoginHistory.objects.create(
                user=user, login_timestamp=datetime.now())
            return redirect('/student-dashboard/')
        else:
            # Authentication failed
            return render(request, 'student_login.html', {'error_message': 'Invalid USN or password'})
    print("test1")

    return render(request, 'student_login.html')


def teacher_login(request):
    if request.method == 'POST':
        # Retrieve data from the form
        faculty_id = request.POST.get('username')
        password = request.POST.get('password')
        print(faculty_id, password)

        # Check if the credentials are valid
        user = authenticate(username=faculty_id, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            # Create a new LoginHistory record for the logged-in user
            LoginHistory.objects.create(
                user=user, login_timestamp=datetime.now())
            # Redirect to a different page after successful login
            return redirect('/faculty-dashboard/')
        else:
            # Authentication failed, display an error message or handle it accordingly
            error_message = "Invalid faculty ID or password."
            return render(request, 'teacher_login.html', {'error_message': error_message})

    # If the request method is GET, render the login page template
    return render(request, 'teacher_login.html')


def forgot_password(request):
    return render(request, 'forgot_password.html', {'form': ForgotPasswordForm()})


def logout_view(request):
    if request.user.is_authenticated:
        # Update the latest LoginHistory record with the logout timestamp
        latest_login = LoginHistory.objects.filter(
            user=request.user).latest('login_timestamp')
        latest_login.logout_timestamp = datetime.now()
        latest_login.save()
        logout(request)
    return redirect('login_page')


def student_dashboard(request):
    student_id = request.user.username  # Assuming username is USN
    print(student_id)
    student = get_object_or_404(Student, USN=student_id)
    print(student)

    sem = request.session.get('sem')  # Assuming you store semester in session

    attendance = Attendance.objects.filter(USN=student_id)
    courses = Course.objects.filter(Sem=sem)
    faculties = Faculty.objects.filter(Dept_ID=student.Dept_ID)
    extracurricular_activities = Extra_Curricular.objects.filter(
        USN=student_id)

    context = {
        'student': student,
        'attendance': attendance,
        'courses': courses,
        'faculties': faculties,
        'extracurricular_activities': extracurricular_activities,
    }

    return render(request, 'student_dashboard.html', context)


def faculty_dashboard(request):
    faculty_id = request.user.username  # Assuming username is Faculty_ID
    faculty = get_object_or_404(Faculty, Faculty_ID=faculty_id)

    # Get the courses assigned to the faculty
    faculty_courses = faculty.Subject_ID.all()

    subjects_per_course = {}
    dept_course_mapping = {}

    # Iterate through each course
    for course in faculty_courses:
        # Get the related subjects for the current course
        subjects = Course.objects.filter(
            Dept_ID=course.Dept_ID, Sem=course.Sem)
        subjects_per_course[course] = subjects
        dept = course.Dept_ID
        if dept:
            if dept not in dept_course_mapping:
                dept_course_mapping[dept] = []
            dept_course_mapping[dept].append(course)
    context = {
        'faculty': faculty,
        'subjects_per_course': subjects_per_course,
        'dept_course_mapping': dept_course_mapping,
    }

    return render(request, 'faculty_dashboard.html', context)


def student_courses(request):
    # Assuming 'usn' is passed as a query parameter or retrieved from the session
    user = request.user.username
    print(user)

    student = Student.objects.get(USN=user)
    print(student)
    subject_ids = student.Subject_ID.all()
    print("hello")
    print(subject_ids)

    faculty_details = []

    # Iterate over the subject IDs and query the Faculty table for each subject
    for subject_id in subject_ids:
        faculty = Faculty.objects.filter(Subject_ID=subject_id).first()
        if faculty:
            faculty_dept = faculty.Dept_ID.first()  # Assuming Dept_ID is a ManyToManyField
            faculty_details.append({
                'subject_id': subject_id,
                'subject_name': subject_id.Subject_Name,
                'dept_id': faculty_dept.Dept_ID,
                'dept_name': faculty_dept.Dept_Name,
                'faculty_id': faculty.Faculty_ID,
                'faculty_name': faculty.Name,
                'qualification': faculty.Qualifications,
                'faculty_email': faculty.Email,
                'phone': faculty.Phone_No
            })

    return render(request, 'student_courses.html', {'faculty_details': faculty_details})


def faculty_course(request):
    user = request.user.username
    print(user)
    faculty = Faculty.objects.get(Faculty_ID=user)
    print(faculty)
    subject_ids = faculty.Subject_ID.all()
    print(subject_ids)

    courses_details = []
    for subject_id in subject_ids:
        courses = Course.objects.filter(Subject_ID=subject_id.pk).first()
        courses_details.append({
            'subject_id': subject_id,
            'subject_name': subject_id.Subject_Name,
            'sem': courses.Sem,
            'dept_id': courses.Dept_ID,
            'dept_name': courses.Dept_ID.Dept_Name
        })

    return render(request, 'faculty_course.html', {'courses_details': courses_details})


def student_attendance(request):
    # Assuming the logged-in user's USN is stored in the username field
    usn = request.user.username

    # Query attendance records for the logged-in user
    attendance_records = Attendance.objects.filter(USN__USN=usn)

    # Calculate attendance percentage for each subject
    subject_attendance = {}
    for record in attendance_records:
        subject = record.Subject_ID
        total_classes = Attendance.objects.filter(
            USN__USN=usn, Subject_ID=subject).count()
        attended_classes = Attendance.objects.filter(
            USN__USN=usn, Subject_ID=subject, Attendance_status='P').count()
        if total_classes > 0:
            attendance_percentage = (attended_classes / total_classes) * 100
        else:
            attendance_percentage = 0
        subject_attendance[subject] = attendance_percentage
        # Create a pie chart for each subject
        plt.figure()
        plt.pie([attended_classes, total_classes - attended_classes], labels=['Attended', 'Absent'],
                autopct='%1.1f%%', startangle=90)
        plt.title(f'Attendance for {subject.Subject_Name}')
        plt.axis('equal')
        filename = f'attendance_pie_chart_{subject.Subject_ID}.png'
        plt.savefig(f'C:\\DBMS_project\\auxilium\\LMS\\static\\{filename}')
        plt.close()

    # Generate HTML table for attendance records
    context = {
        'attendance_records': attendance_records,
        'subject_attendance': subject_attendance,
    }

    return render(request, 'student_attendance.html', context)


def marks_list(request):
    marks = Marks.objects.all()
    return render(request, 'faculty_marks_list.html', {'marks': marks})


def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'faculty_attendance_list.html', {'attendances': attendances})


def marks_add(request):
    if request.method == 'POST':
        usn_id = request.POST.get('usn')
        subject_id_id = request.POST.get('subject_id')
        sem_id = request.POST.get('sem')
        internal_marks = request.POST.get('internal_marks')
        assignment_marks = request.POST.get('assignment_marks')
        seminar_marks = request.POST.get('seminar_marks')
        external_marks = request.POST.get('external_marks')
        final_marks = request.POST.get('final_marks')
        performance = request.POST.get('performance')

        # Check if a Marks object with the same USN and Subject_ID already exists
        existing_marks = Marks.objects.filter(
            USN_id=usn_id, Subject_ID_id=subject_id_id).exists()
        if existing_marks:
            return redirect('faculty_marks_list')

        # Create a new Marks object and save it
        Marks.objects.create(
            USN_id=usn_id,
            Subject_ID_id=subject_id_id,
            Sem=sem_id,
            Internal_Marks=internal_marks,
            Assignment_Marks=assignment_marks,
            Seminar_Marks=seminar_marks,
            External_Marks=external_marks,
            Final_Marks=final_marks,
            Performance=performance
        )
        # Assuming marks_list is the URL name for listing marks
        return redirect('faculty_marks_list')

    students = Student.objects.all()
    usns = []
    for student in students:
        usn = student.USN
        usns.append(usn)
    courses = Course.objects.all()

    subject_ids = []
    for course in courses:
        subject_id = course.Subject_ID
        subject_ids.append(subject_id)

    return render(request, 'faculty_marks_form.html', {'usns': usns, 'subject_ids': subject_ids})


def attendance_add(request):
    if request.method == 'POST':
        usn_id = request.POST.get('usn')
        subject_id_id = request.POST.get('subject_id')
        date = request.POST.get('date')
        attendance_status = request.POST.get('attendance_status')

        # Check if a Marks object with the same USN and Subject_ID already exists
        existing_attendance = Attendance.objects.filter(
            USN_id=usn_id, Subject_ID_id=subject_id_id, Date=date).exists()
        if existing_attendance:
            return redirect('faculty_attendance_list')

        # Create a new Marks object and save it
        Attendance.objects.create(
            USN_id=usn_id,
            Subject_ID_id=subject_id_id,
            Date=date,
            Attendance_status=attendance_status
        )
        # Assuming marks_list is the URL name for listing marks
        return redirect('faculty_attendance_list')

    students = Student.objects.all()
    usns = []
    for student in students:
        usn = student.USN
        usns.append(usn)
    courses = Course.objects.all()

    subject_ids = []
    for course in courses:
        subject_id = course.Subject_ID
        subject_ids.append(subject_id)

    return render(request, 'faculty_attendance_form.html', {'usns': usns, 'subject_ids': subject_ids})


def marks_edit(request, Subject_Name):
    marks = get_object_or_404(Marks, Subject_ID__Subject_Name=Subject_Name)

    if request.method == 'POST':
        marks.Internal_Marks = request.POST.get('Internal_Marks')
        marks.Assignment_Marks = request.POST.get('Assignment_Marks')
        marks.Seminar_Marks = request.POST.get('Seminar_Marks')
        marks.External_Marks = request.POST.get('External_Marks')
        marks.Final_Marks = request.POST.get('Final_Marks')
        marks.Performance = request.POST.get('Performance')

        marks.save()

        # Redirect to marks list page after saving changes
        return redirect('faculty_marks_list')

    return render(request, 'faculty_marks_edit.html', {'marks': marks})


def attendance_edit(request, usn_name, subject_name, date):
    attendance = get_object_or_404(
        Attendance, USN__Name=usn_name, Subject_ID__Subject_Name=subject_name, Date=date)

    if request.method == 'POST':
        attendance.Attendance_status = request.POST.get('attendance_status')
        attendance.save()

        # Redirect to the attendance list page after saving changes
        return redirect('faculty_attendance_list')

    return render(request, 'faculty_attendance_edit.html', {'attendance': attendance})


def marks_delete(request, Subject_Name):
    mark = get_object_or_404(Marks, Subject_ID__Subject_Name=Subject_Name)

    if request.method == 'POST':
        mark.delete()
        return redirect('faculty_marks_list')

    return render(request, 'faculty_marks_delete.html', {'mark': mark})


def attendance_delete(request, usn_name, subject_name, date):
    attendance = get_object_or_404(Attendance, USN__Name=usn_name,
                                   Subject_ID__Subject_Name=subject_name, Date=date)

    if request.method == 'POST':
        attendance.delete()
        return redirect('faculty_attendance_list')

    return render(request, 'faculty_attendance_delete.html', {'attendance': attendance})
