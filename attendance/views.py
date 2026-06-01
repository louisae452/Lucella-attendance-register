from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from .models import Student

# Create your views here.
# def index(request):
#    return HttpResponse("Hello world!")

# View to see home page.
class HomeView(TemplateView):
    template_name = "attendance/home.html"
    
# View to see all students registered.
# Check person is logged in and has required permission(admissions_officer group)



#lass StudentsList(generic.ListView):
#    queryset = Student.objects.all()
#    template_name = "attendance/students_list.html"


@login_required
# @permission_required("student.add_student", raise_exception=True)

def students_list(request):
    students = Student.objects.all()
    
    return render(request, "attendance/students_list.html", {"students":students})
    #return object_list(request, template_name="attendance.students_list,html", queryset=students)
    
