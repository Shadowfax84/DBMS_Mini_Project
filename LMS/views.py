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


def landing_page(request):
    return render(request, 'landing.html')


def home(request):
    return render(request, 'home.html')


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login_page')
    else:
        form = StudentSignupForm()
    return render(request, 'student_signup.html', {'form': form})


def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login_page')
        if request.user.is_authenticated:
            # If the user is already authenticated, redirect to the login page
            return redirect('/login_page/')
    else:
        form = TeacherSignupForm()
        # Query the database to get dept_id values
        Dept_ids = Faculty.objects.values_list('Dept_ID', flat=True).distinct()

    return render(request, 'teacher_signup.html', {'form': form})


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
    student = get_object_or_404(Student, USN=student_id)

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
    

    
    context = {
        'faculty': faculty,
        
       
    }

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


def user_courses(request):
    user_subjects = Course.objects.filter(user=request.user)
    print(user_subjects)

    context = {
        'user_subjects': user_subjects
    }
    return render(request, 'student_courses.html', context)
