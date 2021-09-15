from django import forms
from .models import Subject, Teacher, Student, AllofOutlay

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'payment',)


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'subject', 'address', 'phone_number', 'expirence',)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'study_subject', 'teacher', 'study_days', 'study_type', 'paied_payment', 'phone_number',)


class Outlayform(forms.ModelForm):
    class Meta:
        model = AllofOutlay
        fields = ('name', 'outlay')