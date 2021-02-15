from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Lecturer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Group(models.Model):
    course = models.TextField()
    students = models.ManyToManyField(Student)
    teacher = models.OneToOneField(Lecturer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course}'
