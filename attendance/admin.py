from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    DailyRegister, Email, Parent, Sentemail,
    Student, Subject, Teacher, Timetable,
)


@admin.register(Email)
class EmailAdmin(SummernoteModelAdmin):
    list_display = ['subject',]
    search_fields = ['subject',]
    summernote_fields = ('text')


admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Timetable)
admin.site.register(DailyRegister)
admin.site.register(Sentemail)
