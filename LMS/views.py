from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import StudentSignupForm, TeacherSignupForm
from .forms import ForgotPasswordForm


def landing_page(request):
    return render(request, 'landing.html')


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
            return redirect('home.html')
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
            return redirect('home.html')
        else:
            # Handle invalid login credentials
            return render(request, 'teacher_login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'teacher_login.html')


def forgot_password(request):
    # Handle forgot password logic here
    return render(request, 'forgot_password.html', {'form': ForgotPasswordForm()})
