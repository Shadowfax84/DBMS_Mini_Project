"""
URL configuration for auxilium project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from LMS import views
from LMS.views import *

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path("admin/", admin.site.urls),
    path('login-page/', views.login_page, name='login_page'),
    path('student-login/', views.student_login, name='student_login'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', logout_view, name='logout'),
    path('student-signup/', views.student_signup, name='student_signup'),
    path('teacher-signup/', views.teacher_signup, name='teacher_signup'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('mark-attendance/', MarkAttendanceView.as_view(), name='mark_attendance'),
    path('attendance/', AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/<int:pk>/update/',
         AttendanceUpdateView.as_view(), name='attendance_update'),
    path('attendance/<int:pk>/delete/',
         AttendanceDeleteView.as_view(), name='attendance_delete'),
    path('marks/', views.marks_list, name='marks_list'),
    path('marks/<int:pk>/update/', views.marks_update, name='marks_update'),
    path('marks/<int:pk>/delete/', views.marks_delete, name='marks_delete'),
    # path('faculty_course/', faculty_course, name='faculty_course'),
    path('student-courses/', student_courses, name='student_courses'),
    path('home/', views.home, name='home'),
]
