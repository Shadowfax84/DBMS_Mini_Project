from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render, redirect
from .models import Faculty, Attendance, Course, Extra_Curricular, LoginHistory
from .forms import *
from datetime import datetime
from django.contrib import messages


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
    else:
        form = TeacherSignupForm()
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Create a new LoginHistory record for the logged-in user
            LoginHistory.objects.create(
                user=user, login_timestamp=datetime.now())
            return redirect('/student-dashboard/')
        else:
            return render(request, 'student_login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'student_login.html')


def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Create a new LoginHistory record for the logged-in user
            LoginHistory.objects.create(
                user=user, login_timestamp=datetime.now())
            return redirect('/faculty-dashboard/')
        else:
            return render(request, 'teacher_login.html', {'error': 'Invalid username or password.'})
    else:
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
    return render(request, 'faculty_dashboard.html')


def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'mark_attendance.html', {'form': form, 'attendance_saved': True})
    else:
        form = AttendanceForm()
    return render(request, 'mark_attendance.html', {'form': form, 'attendance_saved': False})


def enter_marks(request):
    popup_message = ''
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            form.save()
            popup_message = 'Marks saved successfully!'
            return redirect('/enter-marks/')

        else:
            popup_message = 'Form validation failed. Please check your input.'
    else:
        form = MarksForm()
    return render(request, 'enter_marks.html', {'form': form, 'popup_message': popup_message})
