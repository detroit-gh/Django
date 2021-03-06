from django import forms

from .models import ContactUs, Group, Lecturer, Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email')


class LecturerForm(forms.ModelForm):

    class Meta:
        model = Lecturer
        fields = ('first_name', 'last_name', 'email')


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('course', 'students', 'teacher')


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'body')
