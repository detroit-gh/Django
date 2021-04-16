from academy.models import Group, Lecturer, Student
from academy.tests.factory import UserFactory

from django.test import TestCase
from django.urls import reverse

import pytest

from pytest_django.asserts import assertTemplateUsed


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


@pytest.fixture
def create_students():
    students = []
    for num_of_stud in range(NUMBER_OF_STUDENTS):
        student = Student.objects.create(first_name=F_NAME, last_name=L_NAME, email=EMAIL)
        students.append(student)
    return students


@pytest.fixture
def create_lecturers():
    lecturers = []
    for num_of_lec in range(NUMBER_OF_TEACHERS):
        lecturer = Lecturer.objects.create(first_name=F_NAME, last_name=L_NAME, email=EMAIL)
        lecturers.append(lecturer)
    return lecturers


@pytest.fixture
def create_groups(create_lecturers):
    groups = []
    for num_of_grp in range(NUMBER_OF_GROUPS):
        group = Group.objects.create(course=COURSE, teacher=create_lecturers[num_of_grp])
        groups.append(group)
    return groups


@pytest.mark.django_db
def test_number_of_students(create_students):
    assert len(create_students) == NUMBER_OF_STUDENTS


@pytest.mark.django_db
def test_view_students_url_exists_at_desired_location(client):
    resp = client.get('/students')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_students_url_accessible_by_name(client):
    resp = client.get(reverse('get_students'))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_students_correct_template(client):
    resp = client.get(reverse('get_students'))
    assert resp.status_code == 200
    assertTemplateUsed(resp, 'academy/students_template.html')


@pytest.mark.django_db
def test_lists_all_students(client, create_students):
    resp = client.get(reverse('get_students'))
    assert resp.status_code == 200
    students = resp.context['students']
    assert len(students) == NUMBER_OF_STUDENTS


@pytest.mark.django_db
def test_number_of_lecturers(create_lecturers):
    assert len(create_lecturers) == NUMBER_OF_TEACHERS


@pytest.mark.django_db
def test_view_lecturers_url_exists_at_desired_location(client):
    resp = client.get('/lecturers')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_lecturers_url_accessible_by_name(client):
    resp = client.get(reverse('get_lecturers'))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_lecturers_correct_template(client):
    resp = client.get(reverse('get_lecturers'))
    assert resp.status_code == 200
    assertTemplateUsed(resp, 'academy/lecturers_template.html')


@pytest.mark.django_db
def test_lists_all_lecturers(client, create_lecturers):
    resp = client.get(reverse('get_lecturers'))
    assert resp.status_code == 200
    lecturers = resp.context['lecturers']
    assert len(lecturers) == NUMBER_OF_TEACHERS


@pytest.mark.django_db
def test_number_of_groups(create_groups):
    assert len(create_groups) == NUMBER_OF_GROUPS


@pytest.mark.django_db
def test_view_groups_url_exists_at_desired_location(client):
    resp = client.get('/groups')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_groups_url_accessible_by_name(client):
    resp = client.get(reverse('get_groups'))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_groups_correct_template(client):
    resp = client.get(reverse('get_groups'))
    assert resp.status_code == 200
    assertTemplateUsed(resp, 'academy/groups_template.html')


@pytest.mark.django_db
def test_lists_all_groups(client, create_groups):
    resp = client.get(reverse('get_groups'))
    assert resp.status_code == 200
    groups = resp.context['groups']
    assert len(groups) == NUMBER_OF_GROUPS


@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        return UserFactory.create(**kwargs)
    return make_user


@pytest.mark.django_db
def test_hide_home_button_on_main_page(client):
    resp = client.get(reverse('get_home'))
    assert resp.status_code == 200
    expected_link = '<a href="{% url ''get_home'' %}">'
    assert expected_link.encode() not in resp.content


@pytest.mark.django_db
def test_hide_student_buttons_for_authenticated_users(client, create_user):
    user = create_user()
    client.force_login(user)
    resp = client.get(reverse('get_students'))
    assert resp.status_code == 200
    expected_add_link = '<a href="{% url ''add_students'' %}">'
    expected_edit_link = '<a href="{% url ''edit_students'' student_id=student.id %}">'
    expected_delete_link = '<a href="{% url ''delete_students'' student_id=student.id %}">'
    assert expected_add_link.encode() not in resp.content
    assert expected_edit_link.encode() not in resp.content
    assert expected_delete_link.encode() not in resp.content


@pytest.mark.django_db
def test_hide_lecturer_buttons_for_authenticated_users(client, create_user):
    user = create_user()
    client.force_login(user)
    resp = client.get(reverse('get_lecturers'))
    assert resp.status_code == 200
    expected_add_link = '<a href="{% url ''add_lecturers'' %}">'
    expected_edit_link = '<a href="{% url ''edit_lecturers'' lecturer_id=lecturer.id %}">'
    expected_delete_link = '<a href="{% url ''delete_lecturers'' lecturer_id=lecturer.id %}">'
    assert expected_add_link.encode() not in resp.content
    assert expected_edit_link.encode() not in resp.content
    assert expected_delete_link.encode() not in resp.content


@pytest.mark.django_db
def test_hide_group_buttons_for_authenticated_users(client, create_user):
    user = create_user()
    client.force_login(user)
    resp = client.get(reverse('get_groups'))
    assert resp.status_code == 200
    expected_add_link = '<a href="{% url ''add_groups'' %}">'
    expected_edit_link = '<a href="{% url ''edit_groups'' group_id=group.id %}">'
    expected_delete_link = '<a href="{% url ''delete_groups'' group_id=group.id %}">'
    assert expected_add_link.encode() not in resp.content
    assert expected_edit_link.encode() not in resp.content
    assert expected_delete_link.encode() not in resp.content
