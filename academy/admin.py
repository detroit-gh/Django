import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import ContactUs, Group, Lecturer, Student


admin.site.register(ContactUs)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    actions = ['export']

    def export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'
        writer = csv.writer(response)
        header = ['FirstName', 'LastName', 'Email']
        writer.writerow(header)
        for student in queryset:
            row = [
                student.first_name,
                student.last_name,
                student.email
            ]
            writer.writerow(row)
        return response

    export.short_description = 'Export students'


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    actions = ['export']

    def export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="lecturers.csv"'
        writer = csv.writer(response)
        header = ['FirstName', 'LastName', 'Email']
        writer.writerow(header)
        for lecturer in queryset:
            row = [
                lecturer.first_name,
                lecturer.last_name,
                lecturer.email
            ]
            writer.writerow(row)
        return response

    export.short_description = 'Export lecturers'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    actions = ['export']

    def export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="groups.csv"'
        writer = csv.writer(response)
        header = ['Course', 'Teacher', 'Students']
        writer.writerow(header)
        for group in queryset:
            row = [
                group.course,
                group.teacher,
                ','.join(group.full_name() for group in group.students.all()),
            ]
            writer.writerow(row)
        return response

    export.short_description = 'Export groups'
