from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Model to store parents details.
class Parent(models.Model):
    """Creates a table of user parents. Requires userrs to be in group parent"""
    parent_name = models.OneToOneField(User, on_delete=models.RESTRICT, limit_choices_to={'groups__name': "parent"})
    phone_number= models.IntegerField()
    
    class Meta:
        ordering = ["parent_name"]
    
    def __str__(self):
        return f"{self.parent_name}"

#  Model to store students' details.

SEX = ((3, "Male"), (2, "Female"))
GROUP = ((0, "Juniors"), (1, "Seniors"))
MUSIC = ((4, "Beginners"), (5, "Advanced"))
OPTION = ((0, "MJB"), (1, "MJA"), (2, "MSB"), (3, "MSA"), (4, "FJB"), (5, "FJA"), (6, "FSB"), (7, "FSA"), (8, "Undetermined"))
class Student(models.Model):
    """Creates a table with students data"""
    student_name = models.CharField(max_length=200)
    student_surname = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    student_code = models.CharField(max_length= 50, unique=True)
    sex = models.IntegerField(choices=SEX, blank=False)
    group = models.IntegerField(choices=GROUP, blank=False)
    music_option = models.IntegerField(choices=MUSIC, blank=False)
    option = models.IntegerField(choices=OPTION, blank=True, null=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    deregistered = models.BooleanField(default=False)
    deregistered_on = models.DateField(blank=True, null=True, default=None)
    parent_name = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "parent"})
    
    class Meta:
        ordering = ["-group", "student_surname"]
    
    def __str__(self):
        return f"{self.group}: {self.student_surname} {self.student_name}"


# Model to store teachers' details.
class Teacher(models.Model):
    """Creates a table of teacher users. Requires users to belong to group teacher"""
    teacher_name = models.OneToOneField(User, on_delete=models.RESTRICT, limit_choices_to={'groups__name': "teacher"})
    phone_number = models.IntegerField(blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.teacher_name}"
    
# Model to store subjects information.
ROOM = ((0, 'English room'), (1, 'Maths room'), (2, 'Lab'), (3, 'Sports Hall'), (4, 'Gym'), (5, 'Music A'), (6, 'Music B'))
SET = ((0, 'Junior'), (1, 'Senior'), (2, 'Female'), (3, 'Male'),
       (4, 'Beginner'), (5, 'Advanced'))

class Subject(models.Model):
    """Creates a table of subject data"""    
    subject_name = models.CharField(max_length=100, unique=True)
    teacher_name = models.ForeignKey(User, on_delete=models.RESTRICT,
                                     limit_choices_to={'groups__name': "teacher"})
    room = models.IntegerField(choices=ROOM, blank=True)  
    set = models.IntegerField(choices=SET, blank=True)
    
    def __str__(self):
        return f"{self.subject_name}"

# Model to show sessions.
SESSION = ((0, 'MomoA'), (1, 'MoafA'), (2, 'TumoA'), (3, 'TuafA'), (4, 'WemoA'), (5, 'WeafA'), (6, 'ThmoA'), (7, 'ThafA'), (8, 'FrmoA'), (9, 'FrafA'), (10, 'MomoB'), (11, 'MoafB'), (12, 'TumoB'), (13, 'TuafB'), (14, 'WemoB'), (15, 'WeafB'), (16, 'ThmoB'), (17, 'ThafB'), (18, 'FrmoB'), (19, 'FrafB'))
DAYS = ((0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"), (4,"Friday"))
TIME = ((0, "Morning"), (1, "Afternoon")) 
TIMETABLEGROUP = ((0, "A"), (1, "B"))     
class Timetable(models.Model):
    """Creates a table showing the days and times the different subjects run"""
    session_id = models.IntegerField(choices=SESSION, blank=True, unique=True)
    day = models.IntegerField(choices=DAYS, blank=True, default=0)
    session = models.IntegerField(choices=TIME, blank=True)
    group = models.IntegerField(choices=TIMETABLEGROUP, blank=True)
    subject_name = models.ForeignKey(Subject, on_delete=models.RESTRICT)
    
    class Meta:
        ordering = ['day', 'session', 'group']
    
    def __str__(self):
        return f"{self.get_day_display()} {self.get_session_display()} Group: {self.get_group_display()}"
    
# Model to record daily attendance.
MARK = ((0, 'Present'), (1, 'Absent'), (2, 'Not recorded '))
STATUS = ((0, 'N/A'), (1, 'Pending'), (2, 'Authorised'), (3, 'Unauthorised'))
ABSENCECODE = ((0, 'Medical'), (1, 'Educational activity'), (2, 'Unauthorised'), (3, ' '))
class DailyRegister(models.Model):
    session_id = models.ForeignKey(Timetable, on_delete=models.RESTRICT)
    date_created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    student_code = models.ForeignKey(Student, on_delete=models.RESTRICT)
    mark = models.IntegerField(choices=MARK, default=2)
    # reason_for_absence = models.CharField(max_length=200, blank=True)
    status = models.IntegerField(choices=STATUS, blank=True, default='0')
    code = models.IntegerField(choices=ABSENCECODE, blank=True, default='3')
    reason_for_absence = models.TextField( blank=True)
    
    class Meta:
        ordering = ['date', 'student_code']
    
    def __str__(self):
        return(f"{self.date}, {self.student_code}, {self.session_id}")

# Model for emails.
SUBJECT= ((0, 'Attendance below 90%'), (1, 'Attendance below 80%'), (2, 'Student missing'), (3, 'Unauthorised absence'))
class Email(models.Model):
    subject = models.IntegerField(choices=SUBJECT)
    text = models.TextField()
    
    def __str__(self):
        return f"{self.get_subject_display()}"
    
class Sentemail(models.Model):
    student_code = models.ForeignKey(Student, on_delete=models.RESTRICT)
    subject = models.ForeignKey(Email, on_delete=models.RESTRICT)
    date_sent = models.DateTimeField(auto_now_add=True)


  
  
  
        
    
                                
                                