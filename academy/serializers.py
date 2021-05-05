from rest_framework.serializers import ModelSerializer

from .models import Group, Lecturer, Student


class StudentSerializer(ModelSerializer):

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'email')


class LecturerSerializer(ModelSerializer):

    class Meta:
        model = Lecturer
        fields = ('id', 'first_name', 'last_name', 'email')


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'course')
