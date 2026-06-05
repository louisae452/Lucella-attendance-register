from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Model to store parents details.
class Parent(models.Model):
    parent_name = models.OneToOneField(User, on_delete=models.RESTRICT, limit_choices_to={'groups__name': "parent"})
    phone_number= models.CharField(max_length=100)
    
    class Meta:
        ordering = ["parent_name"]
    
    def __str__(self):
        return f"{self.parent_name}"



#  Model to store students' details.

SEX = ((0, "Male"), (1, "Female"))
GROUP = ((0, "Juniors"), (1, "Seniors"))
MUSIC = ((0, "Beginers"), (1, "Advanced"))
OPTION = ((0, "MJB"), (1, "MJA"), (2, "MSB"), (3, "MSA"), (4, "FJB"), (5, "FJA"), (6, "FSB"), (7, "FSA"), (8, "Undetermined"))
class Student(models.Model):
    student_name = models.CharField(max_length=200)
    student_surname = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    student_code = models.CharField(max_length= 50, blank=True)
    sex = models.IntegerField(choices=SEX, blank=False)
    group = models.IntegerField(choices=GROUP, blank=False)
    music_option = models.IntegerField(choices=MUSIC, blank=False)
    option = models.IntegerField(choices=OPTION, blank=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    deregistered = models.BooleanField(default=False)
    parent_name = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "parent"})
    
    class Meta:
        ordering = ["-group", "student_surname"]
    
    def __str__(self):
        return f"{self.group}: {self.student_surname} {self.student_name}"


# Model to store teachers' details.

class Teacher(models.Model):
    teacher_name = models.OneToOneField(User, on_delete=models.RESTRICT, limit_choices_to={'groups__name': "teacher"})
    phone_number = models.CharField(max_length=100, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.teacher_name}"
    
    
    
    
    
