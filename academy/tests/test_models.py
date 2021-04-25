from academy.models import Group, Lecturer, Student

from django.core.exceptions import ValidationError
from django.test import TestCase


class AcademyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.first_name = 'Anton'
        cls.last_name = 'Lysenko'
        cls.email = 'anthony@gmail.com'
        cls.course = 'some course'

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_successful_student_creation(self):
        student = Student(first_name=self.first_name, last_name=self.last_name, email=self.email)
        student.full_clean()

    def test_failure_due_to_long_student_first_name(self):
        long_f_name = 'a' * 31
        student = Student(first_name=long_f_name, last_name=self.last_name, email=self.email)
        expected_message = 'Ensure this value has at most 30 characters (it has 31).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            student.full_clean()

    def test_failure_due_to_long_student_last_name(self):
        long_l_name = 'a' * 51
        student = Student(first_name=self.first_name, last_name=long_l_name, email=self.email)
        expected_message = 'Ensure this value has at most 50 characters (it has 51).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            student.full_clean()

    def test_failure_due_to_incorrect_student_email(self):
        mail = 'abc'
        student = Student(first_name=self.first_name, last_name=self.last_name, email=mail)
        expected_message = 'Enter a valid email address.'
        with self.assertRaisesMessage(ValidationError, expected_message):
            student.full_clean()

    def test_successful_lecturer_creation(self):
        lecturer = Lecturer(first_name=self.first_name, last_name=self.last_name, email=self.email)
        lecturer.full_clean()

    def test_failure_due_to_long_lecturer_first_name(self):
        long_f_name = 'a' * 31
        lecturer = Lecturer(first_name=long_f_name, last_name=self.last_name, email=self.email)
        expected_message = 'Ensure this value has at most 30 characters (it has 31).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            lecturer.full_clean()

    def test_failure_due_to_long_lecturer_last_name(self):
        long_l_name = 'a' * 51
        lecturer = Lecturer(first_name=self.first_name, last_name=long_l_name, email=self.email)
        expected_message = 'Ensure this value has at most 50 characters (it has 51).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            lecturer.full_clean()

    def test_failure_due_to_long_lecturer_email(self):
        mail = f'{"a" * 245}@gmail.com'
        lecturer = Lecturer(first_name=self.first_name, last_name=self.last_name, email=mail)
        expected_message = 'Ensure this value has at most 254 characters (it has 255).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            lecturer.full_clean()

    def test_successful_group_creation(self):
        teacher = Lecturer.objects.create(first_name=self.first_name,
                                          last_name=self.last_name,
                                          email=self.email)
        group = Group(course=self.course, teacher=teacher)
        group.full_clean()
