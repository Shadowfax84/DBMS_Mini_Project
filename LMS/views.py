from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from .models import Faculty, Attendance, Course, Extra_Curricular, LoginHistory
from .forms import StudentSignupForm, TeacherSignupForm, ForgotPasswordForm
from datetime import datetime


def landing_page(request):
    return render(request, 'landing.html')


def home(request):
    return render(request, 'home.html')


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            student_group = Group.objects.get(name='Students')
            user.groups.add(student_group)
            return redirect('login_page')
    else:
        form = StudentSignupForm()
    return render(request, 'student_signup.html', {'form': form})


def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            faculty_group = Group.objects.get(name='Faculty')
            user.groups.add(faculty_group)
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
            return redirect('home')
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
    student = request.user.student
    attendance = Attendance.objects.filter(USN=student)
    courses = Course.objects.filter(Sem=student.Sem)
    faculties = Faculty.objects.filter(Dept_ID=student.Dept_ID)
    extracurricular_activities = Extra_Curricular.objects.filter(USN=student)

    context = {
        'student': student,
        'attendance': attendance,
        'courses': courses,
        'faculties': faculties,
        'extracurricular_activities': extracurricular_activities,
    }

    return render(request, 'student_dashboard.html', context)
