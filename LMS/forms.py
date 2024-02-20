from django import forms
from .models import Student, Faculty


class StudentSignupForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['USN', 'Name', 'Sem', 'Gender', 'Phone_No',
                  'Email', 'Joining_Year', 'Dept_ID', 'Subject_ID']
        # Add any additional fields as needed


class TeacherSignupForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['Faculty_ID', 'Name', 'Qualifications',
                  'Papers_Published', 'Phone_No', 'Email', 'Subject_ID', 'Dept_ID']
        # Add any additional fields as needed


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
