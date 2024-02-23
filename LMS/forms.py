from django import forms
from django.contrib.auth.models import User
from .models import Course, Student, Faculty, Attendance, Marks


class StudentSignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, label='Password', required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label='Confirm Password', required=True)
    subject_id = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(), widget=forms.SelectMultiple)
    sem = forms.ModelChoiceField(
        queryset=Course.objects.values_list('Sem', flat=True).distinct(), label='Sem')

    class Meta:
        model = Student
        fields = ['USN', 'Name', 'Gender', 'Phone_No',
                  'Email', 'Joining_Year', 'sem', 'Dept_ID', 'subject_id']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        student = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['USN'], password=self.cleaned_data['password'], email=self.cleaned_data['Email'])
        student.user = user
        if commit:
            student.save()
            self.save_m2m()  # Save many-to-many relationships for subject_id field
        return student


class TeacherSignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, label='Password', required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label='Confirm Password', required=True)

    class Meta:
        model = Faculty
        fields = ['Faculty_ID', 'Name', 'Qualifications', 'Papers_Published',
                  'Phone_No', 'Email', 'Subject_ID', 'Dept_ID']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match. Please enter matching passwords.")

        return cleaned_data

    def save(self, commit=True):
        faculty = super().save(commit=False)
        user = User.objects.create_user(username=self.cleaned_data['Faculty_ID'],
                                        password=self.cleaned_data['password'],
                                        email=self.cleaned_data['Email'])
        faculty.user = user
        if commit:
            faculty.save()
        return faculty


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['USN', 'Subject_ID', 'Date', 'Attendance_status']
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
            'Attendance_status': forms.Select(choices=[('Present', 'Present'), ('Absent', 'Absent')]),
        }


class MarksForm(forms.ModelForm):
    sem = forms.ModelChoiceField(
        queryset=Course.objects.values_list('Sem', flat=True).distinct(), label='Sem')

    class Meta:
        model = Marks
        fields = ['USN', 'Subject_ID', 'sem', 'Internal_Marks', 'Assignment_Marks',
                  'Seminar_Marks', 'External_Marks', 'Final_Marks', 'Performance']
