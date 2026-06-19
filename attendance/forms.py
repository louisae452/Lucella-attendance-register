from .models import Student, Parent, Teacher, Timetable, DailyRegister, Sentemail


from django import forms
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from django.contrib.auth.models import User


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_name', 'student_surname', 'student_code', 'parent_name', 'date_of_birth', 'sex', 'group', 'music_option', 'option',)
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

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('teacher_name', 'phone_number',)

class GetregisterForm(forms.ModelForm):
    
    class Meta:
        model = Timetable
        fields = ('day', 'session', 'subject_name')
             
# Form to get class daily register
#RegisterFormSet = inlineformset_factory(Student, DailyRegister, fields=['student_code','mark'], can_delete=False)
#Need to change in if suff??


#student =Student.objects.get(set=currentset)
#formset= DailyRegisterSet(instance=student)           

#RegisterFormSet = modelformset_factory (DailyRegister, fields=['session_id','mark', 'student_code'], extra=0)


# 
class RegisterForm(forms.ModelForm):
    class Meta:
        model = DailyRegister
        fields=['student_code', 'mark']
    def __init__(self, *for_args, **kwars):
        super().__init__(*for_args, **kwars)
        self.fields['student_code'].disabled = True
        
#create formset class:
RegisterFormSet = modelformset_factory(DailyRegister, form=RegisterForm, extra=0)    

# Create form to send email.
class SendemailForm(forms.ModelForm):
    class Meta:
        model = Sentemail
        fields = ['subject']
        
        
# Form to register an absence.

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = DailyRegister
        fields = ['date', 'reason_for_absence']
# Form to give/edit reason for a past absence.
class GivereasonForm(forms.ModelForm):
    class Meta:
        model = DailyRegister
        fields = ['reason_for_absence']
        
    

        
    
        


        