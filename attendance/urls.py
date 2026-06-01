from . import views
from django.urls import path
from .views import HomeView
#from .views import StudentsList

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('student/', views.students_list, name='students'),
   # path('student/', StudentsList.as_view(), name='students'),
]#