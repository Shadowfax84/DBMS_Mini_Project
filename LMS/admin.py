from django.contrib import admin
from .models import *

for model in [Dept, Course, Student, Faculty, Extra_Curricular, Attendance, Marks, LoginHistory]:
    admin.site.register(model)
