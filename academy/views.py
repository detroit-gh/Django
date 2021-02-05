from django.shortcuts import render
from .models import Student, Lecturer, Group



def get_home(request):
    return render(request, 'academy/home_template.html')


def get_students(request):
    students = Student.objects.all()
    return render(request, 'academy/students_template.html', {'students': students})


def get_lecturers(request):
    lecturers = Lecturer.objects.all()
    return render(request, 'academy/lecturers_template.html', {'lecturers': lecturers})


def get_groups(request):
    groups = Group.objects.all()
    return render(request, 'academy/groups_template.html', {'groups': groups})
