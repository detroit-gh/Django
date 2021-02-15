from academy.models import Group, Lecturer, Student

from django.core.management.base import BaseCommand

from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Add groups, lecturers and students'

    def handle(self, *args, **kwargs):
        for g in range(2):
            lecturer = Lecturer.objects.create(first_name=fake.first_name(),
                                               last_name=fake.last_name(),
                                               email=fake.email()
                                               )
            lecturer.save()
            group = Group.objects.create(course=fake.sentence(nb_words=10), teacher=lecturer)
            for s in range(10):
                student = Student.objects.create(first_name=fake.first_name(),
                                                 last_name=fake.last_name(),
                                                 email=fake.email()
                                                 )
                student.save()
                group.students.add(student)
            group.save()
