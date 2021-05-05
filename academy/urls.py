from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_home, name='get_home'),
    path('students', views.get_students, name='get_students'),
    path('lecturers', views.get_lecturers, name='get_lecturers'),
    path('groups', views.get_groups, name='get_groups'),
    path('students/add', views.add_students, name='add_students'),
    path('lecturers/add', views.add_lecturers, name='add_lecturers'),
    path('groups/add', views.add_groups, name='add_groups'),
    path('students/<int:student_id>/edit', views.edit_students, name='edit_students'),
    path('lecturers/<int:lecturer_id>/edit', views.edit_lecturers, name='edit_lecturers'),
    path('groups/<int:group_id>/edit', views.edit_groups, name='edit_groups'),
    path('students/<int:student_id>/delete', views.delete_students, name='delete_students'),
    path('lecturers/<int:lecturer_id>/delete', views.delete_lecturers, name='delete_lecturers'),
    path('groups/<int:group_id>/delete', views.delete_groups, name='delete_groups'),
    path('contactus', views.add_feedback, name='add_feedback'),
    path('api/v1/students/', views.students),
    path('api/v1/lecturers/', views.lecturers),
    path('api/v1/groups/', views.groups),
    path('api/v1/students/<int:student_id>', views.student),
    path('api/v1/lecturers/<int:lecturer_id>', views.lecturer),
    path('api/v1/groups/<int:group_id>', views.group)
]
