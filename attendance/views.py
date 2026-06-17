from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Student,Timetable, Subject, DailyRegister

from .forms import StudentForm, UserForm, ParentForm, TeacherForm, GetregisterForm, RegisterFormSet, SendemailForm, GetSessionid, AbsenceForm

from django.core.cache import cache


from datetime import date, datetime


# Create your views here.


# View to see home page.
class HomeView(TemplateView):
    template_name = "attendance/home.html"
    


# View to landing page.
class LandingView(TemplateView):
    template_name = "attendance/landing.html"


# View to see all students registered.
@login_required
# @permission_required("student.add_student", raise_exception=True)

def students_list(request):
    students = Student.objects.all()
    for student in students:
        presentdays = DailyRegister.objects.filter(student_code__student_code=student.student_code, mark=0).count()
        totaldays =  DailyRegister.objects.filter(student_code__student_code=student.student_code).count() 
        attendancepercentage = round(((presentdays/totaldays)*100), 2)
        student.attendancepercentage = attendancepercentage
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
@never_cache
def get_register (request):
    cache.clear()
    #getregisterform =GetregisterForm()
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
                new_records_ids= list(DailyRegister.objects.filter(date=today, session_id=currentsessionid).values_list('id', flat=True))
                request.session['filtered_new_records_ids'] = new_records_ids
                # Send the session ids to saveregister view
                return redirect('saveregister')              
    getregisterform =GetregisterForm()                           
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
    today_date = date.today()
    today=datetime.now().date()
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
        del request.session['filtered_new_records_ids']        
        return redirect('landing')
    
    return render(
        request,
        "attendance/daily_register.html",
        {
          'date': today_date,
          'sessionid': sessionid, 
          'register': register,
          'today':today
        }
        )
# View to show student's detail (from teacher landing)
   
def student_detail(request, student_code):
    
    studentname = Student.objects.get(student_code=student_code).student_name
    studentsurname = Student.objects.get(student_code=student_code).student_surname
    studentcode = student_code
    student_records = DailyRegister.objects.filter(student_code__student_code=student_code)
    
    
    return render(
        request,
        "attendance/student_detail.html",
        {
            'studentname': studentname,
            'studentsurname': studentsurname,
            'studentcode': studentcode,
            
            'student_records': student_records
        },
    )
    
    
# View to  send email to parent.
def sendemail(request, student_code):
    form = SendemailForm()
    studentcode =  student_code
    studentname = Student.objects.get(student_code=student_code).student_name
    studentsurname = Student.objects.get(student_code=student_code).student_surname
    if request.method == 'POST':
        parentname = Student.objects.get(student_code=student_code).parent_name
        User = get_user_model()
        parent = User.objects.get(username=parentname)
        parentmail = parent.email
        form = SendemailForm(data=request.POST)
        if form.is_valid():
            sentemail = form.save(commit=False)
            sentemail.student_code = Student.objects.get(student_code=student_code)
            sentemail.save()
            subject = sentemail.subject
            text = sentemail.subject.text
            #Write the email
            text_info = {
                'studentname': studentname,
                'studentsurname': studentsurname,
                'text': text,
            }
            html_content = render_to_string('attendance/email.html', text_info)
            text_content = strip_tags(html_content)
            message = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [parentmail])
            message.attach_alternative(html_content, "text/html")
            message.send()
            #send_mail(subject, html_content, settings.EMAIL_HOST_USER, [parentmail] )
            return redirect('landing')
    return render(
        request,
        "attendance/sendemail.html",
        {
            'form':form,
            'studentcode':studentcode,
            'studentname': studentname,
            'studentsurname': studentsurname,
            
        }
    )        
# Parents pages.
# View to show registered children.
@login_required
def children_list(request):
    
    children = Student.objects.filter(parent_name=request.user)

   
    return render(
        request,
        "attendance/landing.html",
        {
            'children': children,
        }
    )

def landing_router(request, *args, **kwargs):
    if request.user.groups.filter(name='parent').exists():
            
        return children_list(request)
    elif request.user.groups.filter(name='teacher').exists():
        
        return LandingView.as_view()(request, *args, **kwargs)
    
    
# View to see child detail page
def view_child(request, student_code):
    child = Student.objects.get(student_code=student_code)
    return render(
        request,
        "attendance/child_timetable.html",
        {
            'child': child,
        }
        
    )
# View to show childs timetable
def child_timetable(request, student_code):
    child = Student.objects.get(student_code=student_code)
    timetablevalues = {}
    if child.group == 1:
        academicgroupA = ["English A", "Maths A", "Science A"]
        academicrecordsA = Timetable.objects.filter(subject_name__subject_name__in=academicgroupA)
        for record in academicrecordsA:
            # avoids error when passing into next url
            if record.day == 0:
                key=f"M{record.session}"
            else:
                key=f"{record.day}{record.session}"
            timetablevalues[key]=record
    elif child.group == 0:
        academicgroupB = ["English B", "Maths B", "Science B"]
        academicrecordsB = Timetable.objects.filter(subject_name__subject_name__in=academicgroupB)
        for record in academicrecordsB:
            if record.day == 0:
                key=f"M{record.session}"
            else:
                key=f"{record.day}{record.session}"
            timetablevalues[key]=record
    if child.sex == 3:
        record = Timetable.objects.get(subject_name__subject_name="Football A")
        if record.day == 0:
            key=f"M{record.session}"
        else:
            key=f"{record.day}{record.session}"
        timetablevalues[key]=record
    elif child.sex == 2:
        record = Timetable.objects.get(subject_name__subject_name="Athletics B")
        if record.day == 0:
            key=f"M{record.session}"
        else:
            key=f"{record.day}{record.session}"
        timetablevalues[key]=record
    if child.sex == 5:
        record = Timetable.objects.get(subject_name__subject_name="Piano A")
        if record.day == 0:
            key=f"M{record.session}"
        else:
            key=f"{record.day}{record.session}"
        timetablevalues[key]=record
    elif child.music_option == 4:
        record = Timetable.objects.get(subject_name__subject_name="Guitar B")
        if record.day == 0:
            key=f"M{record.session}"
        else:
            key=f"{record.day}{record.session}"
        record.key = key
        timetablevalues[key]=record
        
    return render(
        request,
        "attendance/child_timetable.html",
        {
            'child': child,
            'timetablevalues': timetablevalues,
            
        }
    )
            
                
    







# View to report an absence.
def report_absence(request, student_code, session_id):
   
    child = Student.objects.get(student_code=student_code)
    session = Timetable.objects.get(session_id=session_id)
    
    
    
    
    
    return render(
        request,
        "attendance/report_absence.html",
        {
            'child': child,
            'session': session,
            
        }
    )
    
    
    
    
    
    
