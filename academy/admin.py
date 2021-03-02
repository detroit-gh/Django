from django.contrib import admin

from .models import ContactUs, Group, Lecturer, Student


admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Group)
admin.site.register(ContactUs)
