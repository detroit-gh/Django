from academy.models import Group, Lecturer, Student

from django.test import TestCase
from django.urls import reverse

NUMBER_OF_STUDENTS = 20
NUMBER_OF_TEACHERS = 2
NUMBER_OF_GROUPS = 2
F_NAME = 'Anton'
L_NAME = 'Lysenko'
EMAIL = 'anthony@gmail.com'
COURSE = 'some course'


class StudentListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for num_of_stud in range(NUMBER_OF_STUDENTS):
            Student.objects.create(
                first_name=F_NAME,
                last_name=L_NAME,
                email=EMAIL
            )

    def test_view_students_url_exists_at_desired_location(self):
        resp = self.client.get('/students')
        self.assertEqual(resp.status_code, 200)

    def test_view_students_url_accessible_by_name(self):
        resp = self.client.get(reverse('get_students'))
        self.assertEqual(resp.status_code, 200)

    def test_view_students_correct_template(self):
        resp = self.client.get(reverse('get_students'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'academy/students_template.html')

    def test_lists_all_students(self):
        resp = self.client.get(reverse('get_students'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['students']) == NUMBER_OF_STUDENTS)


class LecturerListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for num_of_lec in range(NUMBER_OF_TEACHERS):
            Lecturer.objects.create(
                first_name=F_NAME,
                last_name=L_NAME,
                email=EMAIL
            )

    def test_view_lecturers_url_exists_at_desired_location(self):
        resp = self.client.get('/lecturers')
        self.assertEqual(resp.status_code, 200)

    def test_view_lecturers_url_accessible_by_name(self):
        resp = self.client.get(reverse('get_lecturers'))
        self.assertEqual(resp.status_code, 200)

    def test_view_lecturers_correct_template(self):
        resp = self.client.get(reverse('get_lecturers'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'academy/lecturers_template.html')

    def test_lists_all_lecturers(self):
        resp = self.client.get(reverse('get_lecturers'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['lecturers']) == NUMBER_OF_TEACHERS)


class GroupListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for num_of_grp in range(NUMBER_OF_GROUPS):
            teacher = Lecturer.objects.create(first_name=F_NAME,
                                              last_name=L_NAME,
                                              email=EMAIL
                                              )
            Group.objects.create(course=COURSE, teacher=teacher)

    def test_view_groups_url_exists_at_desired_location(self):
        resp = self.client.get('/groups')
        self.assertEqual(resp.status_code, 200)

    def test_view_groups_url_accessible_by_name(self):
        resp = self.client.get(reverse('get_groups'))
        self.assertEqual(resp.status_code, 200)

    def test_view_groups_correct_template(self):
        resp = self.client.get(reverse('get_groups'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'academy/groups_template.html')

    def test_lists_all_groups(self):
        resp = self.client.get(reverse('get_groups'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['groups']) == NUMBER_OF_GROUPS)
