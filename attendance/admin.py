from django.contrib import admin
from .models import Student
from .models import Parent
from .models import Teacher
from .models import Subject
from .models import Timetable
from .models import DailyRegister

# Register your models here.
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Timetable)
admin.site.register(DailyRegister)
