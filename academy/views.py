from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from exchanger.models import ExchangeRate

from .forms import ContactUsForm, GroupForm, LecturerForm, StudentForm
from .models import Group, Lecturer, Student


def get_home(request):
    exchange_rates = ExchangeRate.objects.all()
    context = {
        k: v for ex_rate in exchange_rates
        for k, v in ex_rate.to_dict().items()
    }
    return render(request, 'academy/base.html', context)


def get_students(request):
    students = Student.objects.all()
    return render(request, 'academy/students_template.html', {'students': students})


def get_lecturers(request):
    lecturers = Lecturer.objects.all()
    return render(request, 'academy/lecturers_template.html', {'lecturers': lecturers})


def get_groups(request):
    groups = Group.objects.all()
    return render(request, 'academy/groups_template.html', {'groups': groups})


def add_students(request):
    student = None

    if request.method == 'POST':
        student_form = StudentForm(data=request.POST)
        if student_form.is_valid():
            student = student_form.save()
    context = {
        'student': student,
        'student_form': StudentForm()
    }
    return render(request, 'academy/add_students.html', context)


def add_lecturers(request):
    lecturer = None

    if request.method == 'POST':
        lecturer_form = LecturerForm(data=request.POST)
        if lecturer_form.is_valid():
            lecturer = lecturer_form.save()
    context = {
        'lecturer': lecturer,
        'lecturer_form': LecturerForm()
    }
    return render(request, 'academy/add_lecturers.html', context)


def add_groups(request):
    group = None

    if request.method == 'POST':
        group_form = GroupForm(data=request.POST)
        if group_form.is_valid():
            group = group_form.save()
    context = {
        'group': group,
        'group_form': GroupForm()
    }
    return render(request, 'academy/add_groups.html', context)


@cache_page(60 * 30)
def edit_students(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect('get_students')

    form = StudentForm(instance=student)
    return render(request, 'academy/edit_students.html', {'form': form})


@cache_page(60 * 30)
def edit_lecturers(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, id=lecturer_id)
    if request.method == 'POST':
        form = LecturerForm(request.POST, instance=lecturer)
        if form.is_valid():
            lecturer = form.save(commit=False)
            lecturer.save()
            return redirect('get_lecturers')

    form = LecturerForm(instance=lecturer)
    return render(request, 'academy/edit_lecturers.html', {'form': form})


@cache_page(60 * 30)
def edit_groups(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            return redirect('get_groups')

    form = GroupForm(instance=group)
    return render(request, 'academy/edit_groups.html', {'form': form})


def delete_students(request, student_id):
    Student.objects.filter(id=student_id).delete()
    return redirect('get_students')


def delete_lecturers(request, lecturer_id):
    Lecturer.objects.filter(id=lecturer_id).delete()
    return redirect('get_lecturers')


def delete_groups(request, group_id):
    Group.objects.filter(id=group_id).delete()
    return redirect('get_groups')


def add_feedback(request):
    feedback = None
    message = True

    if request.method == 'POST':
        feedback_form = ContactUsForm(data=request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save()
            send = request.session.get('send')
            if send:
                message = True
            else:
                request.session['send'] = True
            request.session.modified = True
    context = {
        'feedback': feedback,
        'feedback_form': ContactUsForm(),
        'send': message
    }
    return render(request, 'academy/add_feedback.html', context)
