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
    sem = forms.ChoiceField(choices=Course.SEMESTER_CHOICES, label='Sem')

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
    widgets = {
        'Dept_ID': forms.Select(attrs={'class': 'frame-413'}),
    }


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
    # def _init_(self, *args, **kwargs):
        # super(AttendanceForm, self)._init_(*args, **kwargs)
    # Query the Student and Course models to get the appropriate choices
        # self.fields['USN'].queryset = Student.objects.all()
        # self.fields['Subject_ID'].queryset = Course.objects.all()


class MarksForm(forms.ModelForm):
    sem = forms.ChoiceField(choices=Course.SEMESTER_CHOICES, label='Sem')

    class Meta:
        model = Marks
        fields = ['USN', 'Subject_ID', 'sem', 'Internal_Marks', 'Assignment_Marks',
                  'Seminar_Marks', 'External_Marks', 'Final_Marks', 'Performance']

    def save(self, commit=True):
        marks_instance = super().save(commit=False)

        # Retrieve the selected semester value from the form
        selected_semester = self.cleaned_data['sem']

        # Get the corresponding Course instance for the selected semester
        course_instance = Course.objects.get(Sem=selected_semester)

        # Assign the Course instance to the 'Sem' field in the 'Marks' model instance
        marks_instance.Sem = course_instance

        if commit:
            marks_instance.save()
        return marks_instance
