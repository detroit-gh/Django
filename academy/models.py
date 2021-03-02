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


class ContactUs(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return f'{self.body}'

    def to_dict(self):
        return{
            'name': self.name,
            'email': self.email,
            'body': self.body
        }
