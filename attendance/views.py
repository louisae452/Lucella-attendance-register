from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import transaction
from django.db.models import Count, Q
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Student,Timetable, Subject, DailyRegister, Sentemail, Email
from .forms import StudentForm, UserForm, ParentForm, TeacherForm, GetregisterForm, RegisterFormSet, SendemailForm, AbsenceForm, GivereasonForm, PendingabsenceForm, GetclassForm, RemoveForm
from django.core.cache import cache
from datetime import date, datetime


# Create your views here.    
def in_teacher(user):
    """Denies permission to users not in teacher group"""
    if user.is_authenticated and user.groups.filter(name='teacher').exists():
        return True
    raise PermissionDenied
def in_parent(user):
    """Denies permission to users not in parent group"""
    if user.is_authenticated and user.groups.filter(name='parent').exists():
        return True
    raise PermissionDenied


class HomeView(TemplateView):
    """
        Renders homepage.
        
        **Template:**
        
        :template:`attendance/home.html`  
    """
    template_name = "attendance/home.html"
    
@method_decorator(login_required, name='dispatch')
class LandingView(TemplateView):
    """
        Renders landing page.
        
        **Template:**
        
        :template:`attendance/landing.html`
    """
    template_name = "attendance/landing.html"



@user_passes_test(in_teacher)
def students_list(request):
    """
        Renders list of all registered students.
        
        **Context**
        
        ``students``
        queryset of registered students,
        
        **Template**
        :template:`attendance/students_list.html`
        
    """
    students = Student.objects.filter(deregistered=False)
    students = students.annotate(
                total_sessions=Count('dailyregister'),
                present_sessions = Count('dailyregister', filter=Q(dailyregister__mark=0)),
            )
    for student in students:
        if student.total_sessions > 0:
            student.attendancepercentage = round((student.present_sessions/student.total_sessions)*100, 2)
        else:
            student.attendancepercentage = 0.0
    return render(request, "attendance/students_list.html", {"students": students})


def add_parent(request):
    """ 
        Adds a new parent user 
        **Context**
        ``userform``
            An instance of :form:`attendance.UserForm]`
            **Template:**
        :template:`attendance.new_parent.html`
    """
    if not (request.user.is_authenticated and request.user.groups.filter(name='admissions_officer').exists()):
        raise PermissionDenied("Only the Admissions Officer has access to this page")
    if request.method == "POST":
        userform = UserForm(data=request.POST)
        if userform.is_valid():
            newuser = userform.save()
            group = Group.objects.get(name="parent")
            newuser.groups.add(group)
            messages.success(request, 'Parent added successfully')
            return redirect('parentdata')
    else:
        userform = UserForm()    
        return render(
            request,
            "attendance/new_parent.html",
            {
                'userform': userform,
            }
    )


def add_parentdata(request):
    """ 
        Adds a extra data to parent user 
        **Context**
        ``parentform``
            An instance of :form:`attnedance.ParentForm``
        **Template:**
        :template:`attendance.parentdata.html`
    """
    if not (request.user.is_authenticated and request.user.groups.filter(name='admissions_officer').exists()):
        raise PermissionDenied("Only the Admissions Officer has access to this page")
    if request.method == "POST":
        parentform = ParentForm(data=request.POST)
        if parentform.is_valid():
            parentform.save()
            messages.success(request, 'Data added successfully')
            return redirect('landing')
    parentform = ParentForm()    
    return render(
        request,
        "attendance/parentdata.html",
        {
            'parentform': parentform,
        }
    )


def add_student(request):
    """ 
        Adds a new student
        
        **Context**
        
        ``studentform``
            An instance of :form:`attnedance.StudentForm``
        
        **Template:**
        
        :template:`attendance.new_student.html`
    """
    if not (request.user.is_authenticated and request.user.groups.filter(name='admissions_officer').exists()):
        raise PermissionDenied("Only the Admissions Officer has access to this page")
    if request.method == "POST":
        studentform = StudentForm(data=request.POST)
        if studentform.is_valid():
            studentform.save()
            messages.success(request, 'Student added successfully')
            return redirect('landing')
    studentform = StudentForm()    
    return render(
        request,
       "attendance/new_student.html",
       {
           'studentform': studentform,
       } 
   )
    

def add_teacher(request):
    """ 
        Adds a new teacher user
        
        **Context**
        
        ``userform``
            An instance of :form:`attendance.UserForm``
        
        **Template:**
        
        :template:`attendance.new_teacher.html`
    """
    if not (request.user.is_authenticated and request.user.groups.filter(name='admissions_officer').exists()):
        raise PermissionDenied("Only the Admissins Officer has access to this page")
    if request.method == "POST":
        userform = UserForm(data=request.POST)
        if userform.is_valid():
            newuser = userform.save()
            group = Group.objects.get(name="teacher")
            newuser.groups.add(group)
            messages.success(request, "Teacher added successfully")
            return redirect('teacherdata')
    userform = UserForm()
    return render(
        request,
        "attendance/new_teacher.html",
        {
            'userform': userform,
        }
    )
    

def add_teacherdata(request):
    """
        Adds extra data to teacher user
        
        **Context**
        
        ``teacherform``
            An instance of :form:`attendance.TeacherForm``
        
        **Template:**
        
        :template:`attendance.teacherdata.html`
    """
    if not (request.user.is_authenticated and request.user.groups.filter(name='admissions_officer').exists()):
        raise PermissionDenied("Only the Admissions Officer has access to this page")
    teacherform = TeacherForm()
    if request.method == "POST":
        teacherform = TeacherForm(data=request.POST)
        if teacherform.is_valid():
            teacherform.save()
            messages.success(request, 'Data added successfully')
            return redirect('landing')
    return render(
        request,
        "attendance/teacherdata.html",
        {
            'teacherform': teacherform,
        }
    )

@never_cache
@user_passes_test(in_teacher)
def get_register (request):
    """
        Collects information about the session in course to produce register.
        
        **Context**
        
        ``getregisterform``
            An instance of :form:`attendance.GetregisterForm`,
        
        **Template**
        
        :template:`attendance/get_register.html`
        
    """
    if request.method == "POST":
        getregisterform = GetregisterForm(data=request.POST)
        if getregisterform.is_valid():
            # Check session is correct
            today = date.today()
            weekday = today.weekday()
            if getregisterform.cleaned_data['day'] == weekday:
                # Find theTimetable record for the current session.
                currentsessionid = get_object_or_404(Timetable, day=getregisterform.cleaned_data['day'], session=getregisterform.cleaned_data['session'], subject_name=getregisterform.cleaned_data['subject_name'])
                # Find the set for the current session
                currentset= get_object_or_404(Subject, subject_name=getregisterform.cleaned_data['subject_name']).set
                # Get the Student records of students on current set
                if currentset == 0 or currentset == 1:
                    students = Student.objects.filter(group=currentset, deregistered=False)
                elif currentset == 2 or currentset == 3:
                    students = Student.objects.filter(sex=currentset, deregistered=False)
                elif currentset == 4 or currentset == 5:
                    students = Student.objects.filter(music_option=currentset, deregistered=False)
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
            else:
                messages.error(request, "Sorry, that session does not exist")
    else:         
            getregisterform =GetregisterForm()                           
    return render(
        request,
        "attendance/get_register.html",
        {
            'getregisterform': getregisterform,
        }
        
    )
    
# View to save the day's register.
@user_passes_test(in_teacher)
def saveregister(request):
    """
        Allows teacher to save the day's register
        
        **Context**
        
        ``date``
            Today's date
        ``sessionid``
            session_id for the session
        ``register``
            An instance of :form:'attendance.RegisterFormSet`
        
        **Template**
        
        :template:`attendance/daily_register.html`
        
    """
    
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
    """
        Shows attendance records of one student.
        **Context**
        ``studentname``
            The name of the student,
        ``studentsurname``
            The surname of the student,
        ``studentcode``
            Sudent_code of the student,
        ``student_records'
            queryset of all the DailyRegister records of the student,
        **Template**
        :template:`attendance/student_detail.html`
    """
    if not (request.user.is_authenticated and request.user.groups.filter(name='attendance_officer').exists()):
        raise PermissionDenied("Only the Attendance Officer has access to this page")
    student = get_object_or_404(Student, student_code=student_code)
    student_records = DailyRegister.objects.filter(student_code=student)
    paginator = Paginator(student_records, 10)
    page_number = request.GET.get("page")
    student_page = paginator.get_page(page_number)
    return render(
        request,
        "attendance/student_detail.html",
        {
            'student': student,
            'student_page': student_page,
        },
    )


def sendemail(request, student_code):
    """
        Sends an email to a parent.
        
        **Context**
        ``userform``
            An instance of :form:`attendance.SendemailForm``
        ``studentcode``
            Sudent_code of the student,
        ``studentname``
            The name of the student,
        ``studentsurname``
            The surname of the student,
        
        **Template**
        
        :template:`attendance/sendemail.html`
    """
    if not (request.user.is_authenticated and request.user.groups.filter(name='attendance_officer').exists()):
        raise PermissionDenied("Only the Attendance Officer has access to this page")    
    student = get_object_or_404(Student, student_code=student_code)
    studentcode = student_code
    studentname = student.student_name
    studentsurname = student.student_surname
    if request.method == 'POST':
        parentname = student.parent_name
        User = get_user_model()
        parent = get_object_or_404(User, username=parentname)
        parentmail = parent.email
        form = SendemailForm(data=request.POST)
        if form.is_valid():
            sentemail = form.save(commit=False)
            sentemail.student_code = student
            sentemail.save()
            subject = sentemail.subject
            text = sentemail.subject.text
            # Write the email
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
            messages.success(request, 'Email sent successfully')
            return redirect('landing')
    form = SendemailForm()
    return render(
        request,
        "attendance/sendemail.html",
        {
            'form': form,
            'studentcode': studentcode,
            'studentname': studentname,
            'studentsurname': studentsurname,
        }
    )        
# Parents pages.

@user_passes_test(in_parent)
def children_list(request):
    """
        Displays a list of all the registered children belonging to a parent user.
        
        **Context**
        
        ``children``
            Queryset of the registered children belonging to the parent user.
        
        **Template:**
        
        :template:`attendance/landing.html`
    """
    children = Student.objects.filter(parent_name=request.user, deregistered=False)
    return render(
        request,
        "attendance/landing.html",
        {
            'children': children,
        }
    )

def landing_router(request, *args, **kwargs):
    """
        Routes the landing view depending on user group
        Prioritises teacher group over parent group
    """
    if request.user.groups.filter(name='parent').exists():
        return children_list(request)
    elif request.user.groups.filter(name='teacher').exists():
        return LandingView.as_view()(request, *args, **kwargs)
    else:
        return redirect('home')

# View to show childs timetable
@user_passes_test(in_parent)
def child_timetable(request, student_code):
    """
        Displays selected child's timetable
        
        **Context**
        
        ``child``
           An instance of student 
        ``timetablevaalues``
            A dictionary of session:subject_name values
        
        **Template:**
        
        :template:`attendance/child_timmetable.html`
    """
    child = get_object_or_404(Student, student_code=student_code)
    timetablevalues = {}
    if child.group == 1:
        academicgroupA = ["English A", "Maths A", "Science A"]
        academicrecordsA = Timetable.objects.filter(subject_name__subject_name__in=academicgroupA)
        for record in academicrecordsA:
            # Avoids error when passing into next url(Will not take an index number starting wiht 0, ie 01)
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
        record = get_object_or_404(Timetable, subject_name__subject_name="Football A")
        if record.day == 0:
            key=f"M{record.session}"
        else:
            key=f"{record.day}{record.session}"
        timetablevalues[key]=record
    elif child.sex == 2:
        record = get_object_or_404(Timetable, subject_name__subject_name="Athletics B")
        if record.day == 0:
            key=f"M{record.session}"
        else:
            key=f"{record.day}{record.session}"
        timetablevalues[key]=record
    if child.music_option == 5:
        record = get_object_or_404(Timetable, subject_name__subject_name="Piano A")
        if record.day == 0:
            key=f"M{record.session}"
        else:
            key=f"{record.day}{record.session}"
        timetablevalues[key]=record
    elif child.music_option == 4:
        record = get_object_or_404(Timetable, subject_name__subject_name="Guitar B")
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
@user_passes_test(in_parent)
def report_absence(request, student_code, session_id):
    """
        Allows parent to report a future absence
        
        **Context**
        
        ``child``
           An instance of Student 
        ``session``
            An instance of Timetable
       ``report``
        An instance of :form:`attendance.AbsenceForm`
        
        **Template:**
        
        :tempalte:`attendance/report_absence.html`
    """
    child = get_object_or_404(Student, student_code=student_code)
    session = get_object_or_404(Timetable, session_id=session_id)
    if request.method == "POST":
        report = AbsenceForm(data=request.POST)
        if report.is_valid():
            absencedate = report.cleaned_data['date']
            dayofweek = absencedate.weekday()
            # Check the  date is the correct weekday.
            if dayofweek == session.day:
                # Check if that absence already exists. Redirect to attendance records if it does.
                if DailyRegister.objects.filter(session_id=session, student_code__student_code=child.student_code, date=absencedate).exists():
                    messages.warning(request, "Absence alreay recorded. Please, access it from the student's records.")
                    return redirect('childdetail', student_code=student_code)
                else:
                    # Create new record with default values
                    newreport = report.save(commit=False)
                    newreport.session_id = session
                    newreport.student_code = child
                    newreport.mark = 1
                    newreport.status = 1
                    newreport.code = 3
                    newreport.save()
                    messages.success(request, "Absence successfully recorded.")
                return redirect ('childdetail', student_code=student_code)
            else:
                # If the specified date is not the correct weekday.
                messages.error(request, 'The date specified does not match a timetable slot!')
                return redirect ('reportabsence', student_code=student_code, session_id=session_id)
    report = AbsenceForm()
    return render(
        request,
        "attendance/report_absence.html",
        {
            'child': child,
            'session': session,
            'report': report,
            
        }
    )
    
# View to show parents their child's attendance record.
@user_passes_test(in_parent)
def child_record(request, student_code):
    """
        Displays individual student's attendance record
        
        **Context**
        
        ``childname``
           Student's name
        ``childsurname``
            Student's surname
        ``childcode``
            Student's code
        ``attendance percentage``
            Student's attendance percentage
       ``childrecords``
            queryset with all the student's DailyRegister records
        
        **Template:**
        
        :template:`attendance/child_record.html`
    """
    student = get_object_or_404(Student, student_code=student_code)
    childname = student.student_name
    childsurname = student.student_surname
    childcode = student_code
    child_records = DailyRegister.objects.filter(student_code__student_code=student_code)
    presentdays = DailyRegister.objects.filter(student_code__student_code=student_code, mark=0).count()
    totaldays =  DailyRegister.objects.filter(student_code__student_code=student_code).count() 
    attendancepercentage = round(((presentdays/totaldays)*100), 2)
    # To show the subject rather than the __str__
    for child in child_records:
        subject = child.session_id.subject_name
        child.subject = subject
    paginator = Paginator(child_records, 10)
    page_number = request.GET.get("page")
    child_page = paginator.get_page(page_number)
    return render(
        request,
        "attendance/child_record.html",
        {
            'childname': childname,
            'childsurname': childsurname,
            'childcode': childcode,
            'attendancepercentage': attendancepercentage,
            'child_page': child_page,
        }
    )
    
# View to edit reason for past absence
@user_passes_test(in_parent)
def give_reason(request, student_code, date, session_id):
    """
        Allows parent to enter a reason for a student's absence
        
        **Context**
        
        ``child``
            An instance of a student
        ``absence``
            An instance of dailyregister
        ``reasonform``
            An instance of :form:`attendance.GivereasonForm`
        
        **Template:**
        
        :template:`attendance/give_reason.html`
    """  
    child = get_object_or_404(Student, student_code=student_code)
    absence = get_object_or_404(DailyRegister, session_id=session_id, date=date, student_code__student_code=student_code)
    if request.method == "POST":
        reasonform = GivereasonForm(data=request.POST, instance=absence)
        if reasonform.is_valid():
            reasonholder = reasonform.save(commit=False)
            # changes status back to pending.
            reasonholder.status = 1
            reasonholder.save()
            messages.success(request, 'Absence saved successfully!')
        return redirect('childrecord', student_code=student_code)
    reasonform = GivereasonForm(instance=absence)            
    return render(
        request,
        "attendance/give_reason.html",
        {
            'child': child,
            'absence': absence,
            'reasonform': reasonform,       
        }
    )
    

def pending_absences(request):
    """
        Displays a list of all pending absences
        
        **Context**
        
        ``pending``
            queryset of all pending instances in DailyRegister
        
        **Template:**
        
        :template:`attendance/pending_absences.html`
    """ 
    if not (request.user.is_authenticated and request.user.groups.filter(name='attendance_officer').exists()):
        raise PermissionDenied("Only the Attendance Officer has access to this page")  
    pending = DailyRegister.objects.filter(status=1)
    return render(
        request,
        "attendance/pending_absences.html",
        {
            'pending': pending,
        }
    )


def absence_detail(request, student_code, date, session_id):
    """
        Allows to review and individual pending absence.
        Sends email to parent when absence is deemed unauthorised
        
        **Context**
        
        ``student``
            An instance of Student
        ``absence``
            An instance of DailyRegister
        ``review`` 
            An instance of |:form:`attendance.PendingabsenceForm
        
        **Template:**
        
        :template:`attendance/absence_detail.html`S
    """  
    if not (request.user.is_authenticated and request.user.groups.filter(name='attendance_officer').exists()):
        raise PermissionDenied("Only the Attendance Officer has access to this page")  
    student = get_object_or_404(Student, student_code=student_code)
    #session = Timetable.objects.get(session_id=session_id)
    absence = get_object_or_404(DailyRegister, student_code__student_code=student_code, session_id=session_id, date=date)
    if request.method == "POST":
        absenceform = PendingabsenceForm(data=request.POST, instance=absence)
        if absenceform.is_valid():
            absenceform.save()
            # Send email if absence is unauthorised
            if absenceform.instance.status == 3:
                parentname = student.parent_name
                User = get_user_model()
                parent = get_object_or_404(User, username=parentname)
                parentmail = parent.email
                email3 = get_object_or_404(Email, subject=3)
                newemail = Sentemail.objects.create(student_code=student, subject=email3)
                text = get_object_or_404(Email, subject=3).text
                subject = newemail.subject
                # Write the email
                text_info = {
                    'studentname': student.student_name,
                    'studentsurname': student.student_surname,
                    'date': absenceform.instance.date,
                    'session': absenceform.instance.session_id,
                    'text': text,
                }
                html_content = render_to_string('attendance/subject3_email.html', text_info)
                text_content = strip_tags(html_content)
                message = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [parentmail])
                message.attach_alternative(html_content, "text/html")
                message.send()
            messages.success(request, "Record successfully updated")
            return redirect('pending')
        else:
            messages.error(request, " Please, fill in all fields in the form")
    else:
        absenceform = PendingabsenceForm(instance=absence)
    return render(
        request,
        "attendance/absence_detail.html",
        {
            'student': student,
            'absence': absence,
            'review': absenceform,
        }
    )

# View to get class list.
@user_passes_test(in_teacher)
def get_class(request):
    """
        Displays a list of all students in a specific class
        
        **Context**
        
        ``classlist``
            instance of :form:attendance.GetclassForm
        
        **Template:**
        
        :template:`attendance/myclass.html`
    """  
    if request.method == "POST":
        classlist = GetclassForm(data=request.POST)
        if classlist.is_valid():
            group = classlist.cleaned_data['subject_name']
            subject = get_object_or_404(Subject, subject_name=group)     
            if subject.set == 0 or subject.set == 1:
                students = Student.objects.filter(group=subject.set, deregistered=False)
                print(students.count())
            elif subject.set == 2 or subject.set == 3:
                students = Student.objects.filter(sex=subject.set, deregistered=False)
            elif subject.set == 4 or subject.set == 5:
                students = Student.objects.filter(music_option=subject.set, deregistered=False)
            # get appropriate session values
            sessionids = Timetable.objects.filter(subject_name__subject_name=group).order_by().values_list('id', flat=True).distinct()
            students = students.annotate(
                total_sessions=Count('dailyregister',
                                     filter=Q(dailyregister__session_id__in=sessionids)),
                present_sessions=Count('dailyregister',
                                       filter=Q(dailyregister__session_id__in= sessionids, dailyregister__mark=0)),
            )
            for student in students:
                student.attendance = round((student.present_sessions/student.total_sessions)*100, 2)
            return render(
                request,
                "attendance/class_list.html",
                {
                    'students': students,
                    'subject': subject,
                }
            )
    classlist = GetclassForm()
    return render(
        request,
        "attendance/myclass.html",
        {
            'classlist': classlist,
        }
    )

# View to see student detail for specific subject.
@user_passes_test(in_teacher)
def class_detail(request, subject_name, student_code):
    """
        Displays to an specific subject of an individual student
        
        **Context**
        
        ``sessionlist``
            queryset of DailyRegister
        ``subjectname``
            name of the subject
        
        **Template:**
        
        :template:`attendance/class_detail.html`
    """  
    sessionids = Timetable.objects.filter(subject_name__subject_name=subject_name).values_list('id', flat=True).distinct()
    sessionslist = DailyRegister.objects.filter(student_code__student_code=student_code, session_id__in=sessionids)
    return render(
        request,
        "attendance/class_detail.html",
        {
            'sessionslist': sessionslist,
            'subject_name': subject_name,
        }
    )


def truanting_list(request):
    """
        Displays a list of all studnets truanting today
        Sends an email to the parent of each student on the list
        
        **Context**
        
        ``truantinglist``
            a queryset of DailyRegister
        ``today``
            today's list
        
        **Template:**
        
        :template:`attendance/truanting_list.html`
    """ 
    if not (request.user.is_authenticated and request.user.groups.filter(name='attendance_officer').exists()):
        raise PermissionDenied("Only the Attendance Officer has access to this page")  
    today = date.today()
    truantinglist = DailyRegister.objects.filter(date=today, mark=1, reason_for_absence='')
    if request.method == "POST":
        # get the email.
        email2 = get_object_or_404(Email, subject=2)
        User = get_user_model()
        # Check all database records at once. abort if one missing.
        with transaction.atomic():  
            for record in truantinglist:   
                student = record.student_code
                parentname = student.parent_name
                parent = User.objects.get(username=parentname)
                parentmail = parent.email
                newemail = Sentemail.objects.create(student_code=student, subject=email2)
                subject = newemail.subject
                # Write the email
                text_info = {
                    'studentname': student.student_name,
                    'studentsurname': student.student_surname,
                    'date': today,
                    'session': record.session_id,
                    'text': email2.text,
                    }
                html_content = render_to_string('attendance/subject3_email.html', text_info)
                text_content = strip_tags(html_content)
                message = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [parentmail])
                message.attach_alternative(html_content, "text/html")
                message.send()
                messages.success(request, 'Email sent successfully')
        return redirect('landing')
    return render(
        request,
        "attendance/truanting.html",
        {
            'truantinglist': truantinglist,
            'today': today,
        }
    )


def remove_student(request):
    """
        Allows Admissions Officer to deregister a student
        
        **Context**
        
        `removeform``
            an instance of :form:'attendance.RemoveForm'
        
        
        **Template:**
        
        :template:`attendance/remove_students.html`
    """  
    if not (request.user.is_authenticated and request.user.groups.filter(name='admissions_officer').exists()):
        raise PermissionDenied("Only the Admissions Officer has access to this page")  
    if request.method == "POST":
        removeform = RemoveForm(data=request.POST)
        if removeform.is_valid():
            student = removeform.cleaned_data.get('student_code')
            student.deregistered_on = date.today()
            student.deregistered = True
            student.save()
            return redirect('landing')
    removeform = RemoveForm()
    return render(
        request,
        "attendance/remove_students.html",
        {
            'removeform': removeform,
        }
    )


 


    
    
