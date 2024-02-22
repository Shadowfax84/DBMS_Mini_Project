from django.db import models
from django.contrib.auth.models import User


class Dept(models.Model):
    Dept_ID = models.IntegerField(primary_key=True)
    Dept_Name = models.CharField(max_length=255)


class Course(models.Model):
    Subject_ID = models.IntegerField(primary_key=True)
    Subject_Name = models.CharField(max_length=255)
    Sem = models.IntegerField()
    Dept_ID = models.ForeignKey(Dept, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    USN = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=255)
    Sem = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='sem_students')
    Gender = models.CharField(max_length=6)
    Phone_No = models.CharField(max_length=10)
    Email = models.EmailField(max_length=255)
    Joining_Year = models.IntegerField()
    Dept_ID = models.ForeignKey(Dept, on_delete=models.CASCADE)
    Subject_ID = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    Faculty_ID = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=255)
    Qualifications = models.CharField(max_length=255)
    Papers_Published = models.IntegerField()
    Phone_No = models.CharField(max_length=10)
    Email = models.EmailField(max_length=255)
    Subject_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    Dept_ID = models.ForeignKey(Dept, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class Extra_Curricular(models.Model):
    USN = models.ForeignKey(Student, on_delete=models.CASCADE)
    Coordinator_ID = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    Event_ID = models.IntegerField(primary_key=True)
    Event_Name = models.CharField(max_length=255)
    Circulars = models.CharField(max_length=255)
    Extra_Curricular_Score = models.IntegerField()


class Attendance(models.Model):
    USN = models.ForeignKey(Student, on_delete=models.CASCADE)
    Subject_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    Date = models.DateField()
    Attendance_status = models.CharField(max_length=10)
    Behaviour_Score = models.IntegerField()
    Attendance_Score = models.IntegerField()


class Marks(models.Model):
    USN = models.ForeignKey(Student, on_delete=models.CASCADE)
    Subject_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    Sem = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='sem_marks')
    Internal_Marks = models.IntegerField()
    Assignment_Marks = models.IntegerField()
    Seminar_Marks = models.IntegerField()
    External_Marks = models.IntegerField()
    Final_Marks = models.IntegerField()
    Performance = models.IntegerField()


class Login(models.Model):
    Username = models.CharField(max_length=255, primary_key=True)
    Password = models.CharField(max_length=255)
