from .models import Student
from .models import Parent

from django import forms
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_name', 'student_surname', 'student_code', 'parent_name', 'date_of_birth', 'sex', 'group', 'music_option', )
        help_texts = {
            'student_code': 'The student code is the last two digits of the year of birth, month of birth, first two letters of surname followed by first two letters of name in capitals.',
        }          

                  
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)
        help_texts = {
            'username': 'The user name is the name followed by surname wihtout spaces',
        }
        
class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ('parent_name', 'phone_number',)         
