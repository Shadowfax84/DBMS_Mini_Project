from django import forms
from django.contrib.auth.models import User
from .models import Student, Faculty


class StudentSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Student
        fields = ['username', 'password', 'USN', 'Name', 'Gender', 'Phone_No',
                  'Email', 'Joining_Year', 'Dept_ID', 'Subject_ID']

    def save(self, commit=True):
        student = super().save(commit=False)
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        password=self.cleaned_data['password'],
                                        email=self.cleaned_data['email'])
        student.user = user
        if commit:
            student.save()
        return student


class TeacherSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Faculty
        fields = ['username', 'password', 'Faculty_ID', 'Name', 'Qualifications',
                  'Papers_Published', 'Phone_No', 'Email', 'Subject_ID', 'Dept_ID']

    def save(self, commit=True):
        faculty = super().save(commit=False)
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        password=self.cleaned_data['password'])
        faculty.user = user
        if commit:
            faculty.save()
        return faculty


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
