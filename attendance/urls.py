from . import views
from django.urls import path
from .views import HomeView
from .views import LandingView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('student/', views.student_detail, name='studentdetail'),
    path('absence/<str:student_code>/', views.report_absence, name='absence'),
    # ???
    path('daiyly_register/', views.get_register, name='dailyregister'),
    path('getregister', views.get_register, name='getregister'),
    path('landing/', views.landing_router, name='landing'),
    path('newparent/', views.add_parent, name='newparent'),
    path('newstudent/', views.add_student, name='newstudent'),
    path('newteacher/', views.add_teacher, name='newteacher'),
    path('parentdata/', views.add_parentdata, name='parentdata'),
    path('student/', views.students_list, name='students'),
    path('teacherdata/', views.add_teacherdata, name='teacherdata'),
    path('saveregister/', views.saveregister, name='saveregister'),
    path('child/<str:student_code>/', views.child_timetable, name='childdetail'),
    path('child/<str:student_code>/<int:session_id>/', views.report_absence, name='reportabsence'),
    path('child/<str:student_code>/record/', views.child_record, name='childrecord'),
    path('child/<str:student_code>/reocrd/<str:date>/<int:session_id>/', views.give_reason, name='givereason'),
    path('student/<str:student_code>/', views.student_detail, name='studentdetail'),
    path('email/<str:student_code>/', views.sendemail, name='sendemail'),
    
   
]