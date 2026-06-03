from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from .models import Student
from .forms import StudentForm
from .forms import UserForm
from .forms import ParentForm

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
 
#View to add a student.
#login_required

def add_parent(request):
    userform = UserForm()
    if request.method == "POST":
        userform = UserForm(data=request.POST)
        if userform.is_valid():
            user = userform.save()
            group = Group.objects.get(name="parent")
            user.groups.add(group)
         
            return redirect('landing')
    
    return render(
        request,
        "attendance/new_parent.html",
        {
            'userform':userform,
            #'parentform': parentform
        }
    )
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
