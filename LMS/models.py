from django.db import models
from django.contrib.auth.models import User


class Dept(models.Model):
    Dept_ID = models.IntegerField(primary_key=True)
    Dept_Name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.Dept_ID)


class Course(models.Model):
    SEMESTER_CHOICES = [
        ('1', '1st Semester'),
        ('2', '2nd Semester'),
        ('3', '3rd Semester'),
        ('4', '4th Semester'),
        ('5', '5th Semester'),
        ('6', '6th Semester'),
        ('7', '7th Semester'),
        ('8', '8th Semester'),
    ]

    Subject_ID = models.IntegerField(primary_key=True)
    Subject_Name = models.CharField(max_length=255)
    Sem = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    Dept_ID = models.ForeignKey(Dept, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Subject_ID)

    def get_semester_choices(self):
        return dict(self.SEMESTER_CHOICES)


class Student(models.Model):
    USN = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=255)
    Sem = models.ForeignKey(Course, on_delete=models.CASCADE,
                            related_name='sem_students', null=True, blank=True)
    Gender = models.CharField(max_length=6, choices=[(
        'male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    Phone_No = models.CharField(max_length=10)
    Email = models.EmailField(max_length=255)
    Joining_Year = models.IntegerField()
    Dept_ID = models.ForeignKey(Dept, on_delete=models.CASCADE)
    Subject_ID = models.ManyToManyField(
        Course, related_name='student_subjects')

    def __str__(self):
        return self.Name


class Faculty(models.Model):
    Faculty_ID = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=255)
    Qualifications = models.CharField(max_length=6, choices=[
        ('b.e', 'B.E'), ('b.sc', 'B.Sc'), ('m.tech', 'M.Tech'), ('m.sc', 'M.Sc'), ('phd', 'PhD')])
    Papers_Published = models.IntegerField()
    Phone_No = models.CharField(max_length=10)
    Email = models.EmailField(max_length=255)
    Subject_ID = models.ManyToManyField(
        Course, related_name='faculty_subjects')
    Dept_ID = models.ManyToManyField(Dept, related_name='faculty_depts')

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
    Attendance_status = models.CharField(max_length=2, choices=[
        ('P', 'Present'), ('AB', 'Absent')])
    Behaviour_Score = models.IntegerField(null=True)
    Attendance_Score = models.IntegerField(null=True)

    def __str__(self):
        return self.USN.Name+" - "+self.Subject_ID.Subject_Name


class Marks(models.Model):
    USN = models.ForeignKey(Student, on_delete=models.CASCADE)
    Subject_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    Sem = models.CharField(max_length=15, choices=Course.SEMESTER_CHOICES)
    Internal_Marks = models.IntegerField()
    Assignment_Marks = models.IntegerField()
    Seminar_Marks = models.IntegerField()
    External_Marks = models.IntegerField()
    Final_Marks = models.IntegerField()
    Performance = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.Subject_ID.Subject_Name} "


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_timestamp = models.DateTimeField(auto_now_add=True)
    logout_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-login_timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.login_timestamp}"
