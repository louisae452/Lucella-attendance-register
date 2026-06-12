from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from .models import Student
from .models import Timetable
from .models import Subject
from .models import DailyRegister
from .forms import StudentForm
from .forms import UserForm
from .forms import ParentForm
from .forms import TeacherForm
from .forms import GetregisterForm

from .forms import RegisterForm
from .forms import RegisterFormSet
from datetime import date

# Create your views here.


# View to see home page.
class HomeView(TemplateView):
    template_name = "attendance/home.html"
    

# Check person is logged in and has required permission(admissions_officer group)


# View to landing page.
class LandingView(TemplateView):
    template_name = "attendance/landing.html"


# View to see all students registered.
@login_required
# @permission_required("student.add_student", raise_exception=True)

def students_list(request):
    students = Student.objects.all()
    
    return render(request, "attendance/students_list.html", {"students":students})
    #return object_list(request, template_name="attendance.students_list,html", queryset=students)
 
#View to add a parent.
#login_required

def add_parent(request):
    userform = UserForm()
    
    if request.method == "POST":
        userform = UserForm(data=request.POST)
        if userform.is_valid():
            newuser = userform.save()
            group = Group.objects.get(name="parent")
            newuser.groups.add(group)
            return redirect('parentdata')
    
    return render(
        request,
        "attendance/new_parent.html",
        {
            'userform': userform,
        }
    )
# View to add additional data for parents. 
def add_parentdata(request):
    parentform = ParentForm()
    if request.method == "POST":
        parentform = ParentForm(data=request.POST)
        if parentform.is_valid():
            parentform.save()
            return redirect('landing')
    return render(
        request,
        "attendance/parentdata.html",
        {
            'parentform': parentform,
        }
    )

# View to add a student

def add_student(request):
    studentform = StudentForm
    if request.method == "POST":
        studentform = StudentForm(data=request.POST)
        if studentform.is_valid():
            studentform.save()
            return redirect('landing')
    return render(
        request,
       "attendance/new_student.html",
       {
           'studentform': studentform,
       } 
   )
    
#View to add a teacher.
def add_teacher(request):
    userform = UserForm()
    
    if request.method == "POST":
        userform = UserForm(data=request.POST)
        if userform.is_valid():
            newuser = userform.save()
            group = Group.objects.get(name="teacher")
            newuser.groups.add(group)
            return redirect('teacherdata')
    
    return render(
        request,
        "attendance/new_teacher.html",
        {
            'userform': userform,
        }
    )
    
# View to add additional data to teacher
def add_teacherdata(request):
    teacherform = TeacherForm()
    if request.method == "POST":
        teacherform = TeacherForm(data=request.POST)
        if teacherform.is_valid():
            teacherform.save()
            return redirect('landing')
    return render(
        request,
        "attendance/teacherdata.html",
        {
            'teacherform': teacherform,
        }
    )
    
# View to get class register
def get_register (request):
    getregisterform =GetregisterForm()
    if request.method == "POST":
        getregisterform = GetregisterForm(data=request.POST)
        if getregisterform.is_valid():
            # Check session is correct
            today = date.today()
            weekday = today.weekday()
            if getregisterform.cleaned_data['day'] == weekday:
                # Find theTimetable record for the current session.
                currentsessionid = Timetable.objects.get(day=getregisterform.cleaned_data['day'], session=getregisterform.cleaned_data['session'], subject_name=getregisterform.cleaned_data['subject_name'])
                # Find the set for the current session
                currentset= Subject.objects.get(subject_name=getregisterform.cleaned_data['subject_name']).set
                # Get the Student records of students on current set
                if currentset == 0 or currentset == 1:
                    students = Student.objects.filter(group=currentset)
                elif currentset == 2 or currentset == 3:
                    students = Student.objects.filter(sex=currentset)
                elif currentset == 4 or currentset == 5:
                    students = Student.objects.filter(music_option=currentset)
                # If a DailyAttendance record for that student and session does not exists, create one with default values.
                for student in students:
                    student_record = DailyRegister.objects.filter(session_id=currentsessionid, date=today, student_code=student).exists()
                    if  not student_record: 
                        new_record = DailyRegister(session_id=currentsessionid, date=today, student_code=student)
                        new_record.save()
                #  Get ids for all the DailyRegister records for current session and set.      
                new_records_ids= list(DailyRegister.objects.filter(date=today).values_list('id', flat=True))
                request.session['filtered_new_records_ids'] = new_records_ids
                # Send the session ids to saveregister view
                return redirect('saveregister')              
                               
    return render(
        request,
        "attendance/get_register.html",
        {
            'getregisterform': getregisterform,
        }
        
    )
    
# View to save the day's register.
def saveregister(request):
   id_list = request.session.get('filtered_new_records_ids',[])
   
   daily_records= DailyRegister.objects.filter(id__in=id_list)
   # Get todays date
   today = date.today()
   # Get session info
   sessionid = daily_records.first().session_id 
   # Get register
   register = RegisterFormSet(queryset=daily_records)
   
   if request.method == "POST":
       register=RegisterFormSet(data=request.POST)
       if register.is_valid():
            for form in register:
                
                instance = form.save(commit=False)
                if instance.mark == 1:
                    instance.status = 1
                instance.save()
       return redirect('landing')
   
   
   
   
   
   
   return render (
        request,
  
        "attendance/daily_register.html",
        {
            'date': today,
            'sessionid': sessionid,
            
            
            
            'register': register
        }
        )