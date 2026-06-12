from . import views
from django.urls import path
from .views import HomeView
from .views import LandingView

#from .views import StudentsList

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('daiyly_register/', views.get_register, name='dailyregister'),
    path('getregister', views.get_register, name='getregister'),
    path('landing/', LandingView.as_view(), name='landing'),
    path('newparent/', views.add_parent, name='newparent'),
    path('newstudent/', views.add_student, name='newstudent'),
    path('newteacher/', views.add_teacher, name='newteacher'),
    path('parentdata/', views.add_parentdata, name='parentdata'),
    path('student/', views.students_list, name='students'),
    path('teacherdata/', views.add_teacherdata, name='teacherdata'),
    #path('file/', views.get_register, name='test'),
    path('saveregister/', views.saveregister, name='saveregister'),
    
   
]