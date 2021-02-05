from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()


class Lecturer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()


class Group(models.Model):
    course = models.TextField()
    students = models.ManyToManyField(Student)
    teacher = models.OneToOneField(Lecturer, on_delete=models.CASCADE)
