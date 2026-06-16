from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Student
from .models import Parent
from .models import Teacher
from .models import Subject
from .models import Timetable
from .models import DailyRegister
from .models import Email
from .models import Sentemail

@admin.register(Email)
class EmailAdmin(SummernoteModelAdmin):
    list_display = ['subject',]
    search_fields = ['subject',]
    summernote_fields = ('text')

# Register your models here.

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Timetable)
admin.site.register(DailyRegister)
admin.site.register(Sentemail)
