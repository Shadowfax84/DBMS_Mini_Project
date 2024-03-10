from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from datetime import datetime
from django.contrib import messages
from .forms import AttendanceForm
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import TeacherSignupForm
from .models import Faculty
from django.http import HttpResponseForbidden


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

        # Authenticate the user
        user = authenticate(request, username=usn, password=password)

        if user is not None:
            login(request, user)
            # Create a new LoginHistory record for the logged-in user
            LoginHistory.objects.create(
                user=user, login_timestamp=datetime.now())
            return redirect('/student-dashboard/')
        else:
            # Authentication failed
            return render(request, 'student_login.html', {'error_message': 'Invalid USN or password'})

    return render(request, 'student_login.html')


def teacher_login(request):
    if request.method == 'POST':
        # Retrieve data from the form
        faculty_id = request.POST.get('username')
        password = request.POST.get('password')

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
    print(faculty_id)
    faculty = get_object_or_404(Faculty, Faculty_ID=faculty_id)
    print(faculty)

    # courses_taught = Course.objects.filter(faculty=faculty)

    # context = {
    # 'faculty': faculty,
    # 'courses_taught': courses_taught,
    # }

    return render(request, 'faculty_dashboard.html')


class MarkAttendanceView(View):
    template_name = 'mark_attendance.html'

    def get(self, request):
        # Get existing USN and Subject IDs from the database
        usn_list = Attendance.objects.values_list('USN', flat=True).distinct()
        subject_id_list = Attendance.objects.values_list(
            'Subject_ID', flat=True).distinct()

        context = {
            'usn_list': usn_list,
            'subject_id_list': subject_id_list,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        usn_id = request.POST.get('usn')
        subject_id = request.POST.get('subjectId')
        date_str = request.POST.get('date')
        attendance_status = request.POST.get('attendanceStatus')

        # Parse date string to datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        try:
            # Retrieve Student object
            student = get_object_or_404(Student, USN=usn_id)

            # Create or update attendance record
            Attendance.objects.create(
                USN=student,
                Subject_ID_id=subject_id,
                Date=date,
                Attendance_status=attendance_status
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


class AttendanceListView(ListView):
    model = Attendance
    template_name = 'attendance_list.html'  # Create this template
    context_object_name = 'attendances'


class AttendanceUpdateView(UpdateView):
    model = Attendance
    fields = ['USN', 'Subject_ID', 'Date', 'Attendance_status']
    template_name = 'attendance_update.html'
    success_url = reverse_lazy('attendance_list')

    def form_valid(self, form):
        # Get the instance of the Attendance object being updated
        attendance_instance = form.save(commit=False)

        # Perform any additional logic here, such as updating values
        # For example, to update the Date field:
        new_date = form.cleaned_data['date']
        attendance_instance.date = new_date

        # Update the Attendance_status field
        new_attendance_status = form.cleaned_data['attendance_status']
        attendance_instance.attendance_status = new_attendance_status

        # Save the updated instance to the database
        attendance_instance.save()

        # Call the superclass's form_valid method to handle the rest of the logic
        return super().form_valid(form)


class AttendanceDeleteView(DeleteView):
    model = Attendance
    # Specify the path to the template
    template_name = 'attendance_confirm_delete.html'
    # Redirect to attendance list page after successful deletion
    success_url = reverse_lazy('attendance_list')


def marks_list(request):
    marks = Marks.objects.all()
    return render(request, 'marks.html', {'marks': marks})


def marks_update(request, pk):
    mark = get_object_or_404(Marks, pk=pk)
    form = MarksForm(request.POST or None, instance=mark)
    if form.is_valid():
        form.save()
        return redirect('marks_list')
    return render(request, 'marks_form.html', {'form': form})


def marks_delete(request, pk):
    mark = get_object_or_404(Marks, pk=pk)
    if request.method == 'POST':
        mark.delete()
        return redirect('marks_list')
    return render(request, 'marks_confirm_delete.html', {'mark': mark})


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
    print(faculty_details)

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
