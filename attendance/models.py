from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Model to store parents details.
class Parent(models.Model):
    parent_name = models.OneToOneField(User, on_delete=models.RESTRICT, limit_choices_to={'groups__name': "parent"})
    phone_number= models.IntegerField()
    
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
    phone_number = models.IntegerField(blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.teacher_name}"
    
# Model to store subjects information.
ROOM = ((0, 'English room'), (1, 'Maths room'), (2, 'Lab'), (3, 'Sports Hall'), (4, 'Gym'), (5, 'Music A'), (6, 'Music B'))
SET = ((0, 'Junior'), (1, 'Senior'), (2, 'Girls'), (3, 'Boys'),
       (4, 'Beginner'), (5, 'Advanced'))

class Subject(models.Model):
    
    subject_name = models.CharField(max_length=100)
    teacher_name = models.ForeignKey(User, on_delete=models.RESTRICT,
                                     limit_choices_to={'groups__name': "teacher"})
    room = models.IntegerField(choices=ROOM, blank=True)  
    set = models.IntegerField(choices=SET, blank=True)
    
    def __str__(self):
        return f"{self.subject_name} {self.set}"


SESSION = ((0, 'MomoA'), (1, 'MoafA'), (2, 'TumoA'), (3, 'TuafA'), (4, 'WemoA'), (5, 'WeafA'), (6, 'ThmoA'), (7, 'ThafA'), (8, 'FrmoA'), (9, 'FrafA'), (10, 'MomoB'), (11, 'MoafB'), (12, 'TumoB'), (13, 'TuafB'), (14, 'WemoB'), (15, 'WeafB'), (16, 'ThmoB'), (17, 'ThafB'), (18, 'FrmoB'), (19, 'FrafB'))
DAYS = ((1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'))
TIME = ((0, 'Morning'), (1, 'Afternoon')) 
TIMETABLEGROUP = ((0,'A'), (1, 'B'), (2, 'TBA'))       
class Timetable(models.Model):
    session_id = models.IntegerField(choices=SESSION, blank=True)
    day = models.IntegerField(choices=DAYS, blank=True, default=0)
    session = models.IntegerField(choices=TIME, blank=True)
    group = models.IntegerField(choices=TIMETABLEGROUP, blank=True)
    subject_name = models.ForeignKey(Subject, on_delete=models.RESTRICT)
    
    def __str__(self):
        return f"{self.day} {self.session}"