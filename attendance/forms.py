from .models import Student
from .models import Parent

from django import forms
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_name', 'student_surname', 'student_code', 'parent_name', 'date_of_birth', 'sex', 'group', 'music_option', )
                  
class UserNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
 
                  
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)
        
class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ('parent_name', 'phone_number',)         
