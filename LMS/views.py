from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Student, Faculty
from .forms import StudentSignupForm, TeacherSignupForm
from .forms import ForgotPasswordForm
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from .models import Attendance, Course, Faculty, Extra_Curricular


def landing_page(request):
    return render(request, 'landing.html')


def home(request):
    return render(request, 'home.html')


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to student dashboard or login page
            return redirect('login_page')
    else:
        form = StudentSignupForm()
    return render(request, 'student_signup.html', {'form': form})


def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to teacher dashboard or login page
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
            # Redirect to student dashboard or desired page
            return redirect('/student-dashboard/')
        else:
            # Handle invalid login credentials
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
            # Redirect to teacher dashboard or desired page
            return redirect('home')
        else:
            # Handle invalid login credentials
            return render(request, 'teacher_login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'teacher_login.html')


def forgot_password(request):
    # Handle forgot password logic here
    return render(request, 'forgot_password.html', {'form': ForgotPasswordForm()})


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
