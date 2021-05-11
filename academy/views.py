from LMS.settings import GROUPS_PER_PAGE, LECTURERS_PER_PAGE, SECRET_KEY, STUDENTS_PER_PAGE

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from exchanger.models import ExchangeRate

import jwt

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler

from .forms import ContactUsForm, GroupForm, LecturerForm, StudentForm
from .models import Group, Lecturer, Student
from .serializers import GroupSerializer, LecturerSerializer, StudentSerializer


def get_home(request):
    exchange_rates = ExchangeRate.objects.all()
    context = {
        k: v for ex_rate in exchange_rates
        for k, v in ex_rate.to_dict().items()
    }
    return render(request, 'academy/base.html', context)


def get_students(request):
    students = Student.objects.all()
    paginator = Paginator(students, STUDENTS_PER_PAGE)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    context = {
        'students': students,
        'page': page
    }
    return render(request, 'academy/students_template.html', context)


def get_lecturers(request):
    lecturers = Lecturer.objects.all()
    paginator = Paginator(lecturers, LECTURERS_PER_PAGE)
    page = request.GET.get('page')
    lecturers = paginator.get_page(page)
    context = {
        'lecturers': lecturers,
        'page': page
    }
    return render(request, 'academy/lecturers_template.html', context)


def get_groups(request):
    groups = Group.objects.all()
    paginator = Paginator(groups, GROUPS_PER_PAGE)
    page = request.GET.get('page')
    groups = paginator.get_page(page)
    context = {
        'groups': groups,
        'page': page
    }
    return render(request, 'academy/groups_template.html', context)


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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
    message = False

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


@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def students(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        rdata = request.data
        data = {
            'first_name': rdata.get('first_name'),
            'text': rdata.get('last_name'),
            'email': rdata.get('email'),
        }
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def student(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    if request.method == 'DELETE':
        student.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        first_name = request.data.get('first_name')
        if first_name:
            student.first_name = first_name
        last_name = request.data.get('last_name')
        if last_name:
            student.last_name = last_name
        email = request.data.get('email')
        if email:
            student.email = email
        student.save()
        return Response(status=HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def lecturers(request):
    if request.method == 'GET':
        lecturers = Lecturer.objects.all()
        serializer = LecturerSerializer(lecturers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        rdata = request.data
        data = {
            'first_name': rdata.get('first_name'),
            'text': rdata.get('last_name'),
            'email': rdata.get('email'),
        }
        serializer = LecturerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def lecturer(request, lecturer_id):
    try:
        lecturer = Lecturer.objects.get(pk=lecturer_id)
    except Lecturer.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LecturerSerializer(lecturer)
        return Response(serializer.data)

    if request.method == 'DELETE':
        lecturer.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        first_name = request.data.get('first_name')
        if first_name:
            lecturer.first_name = first_name
        last_name = request.data.get('last_name')
        if last_name:
            lecturer.last_name = last_name
        email = request.data.get('email')
        if email:
            lecturer.email = email
        lecturer.save()
        return Response(status=HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def groups(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        rdata = request.data
        data = {
            'course': rdata.get('course')
        }
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group(request, group_id):
    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    if request.method == 'DELETE':
        group.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        course = request.data.get('course')
        if course:
            group.course = course
        group.save()
        return Response(status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def authenticate_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        res = {'error': 'Please provide an email and a password'}
        return Response(res)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        message = "Can't find user with the specified email"
        res = {'error': message}
        return Response(res, status=HTTP_404_NOT_FOUND)

    if not user.check_password(password):
        message = "Can't authenticate with the given credentials or the account has " \
                  "been deactivated"
        res = {'error': message}
        return Response(res, status=HTTP_403_FORBIDDEN)

    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, SECRET_KEY)
    user_details = {
        'user_id': user.pk,
        'name': f'{user.first_name} {user.last_name}',
        'token': token
    }
    return Response(user_details, status=HTTP_200_OK)
