from .models import Student, Parent, Teacher, Timetable, DailyRegister, Sentemail, Subject


from django import forms
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from django.contrib.auth.models import User

# Form to add a new student
class StudentForm(forms.ModelForm):
    """Form to add a new student. Requires parent to be a user with group parent"""
    class Meta:
        model = Student
        fields = ('student_name', 'student_surname', 'student_code', 'parent_name', 'date_of_birth', 'sex', 'group', 'music_option',)
        help_texts = {
            'student_code': 'The student code is the last two digits of the year of birth, month of birth, first two letters of surname followed by first two letters of name in capitals.',
        }          

                  
class UserForm(forms.ModelForm):
    """Form to add a new user."""
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)
        help_texts = {
            'username': 'The user name is the name followed by surname wihtout spaces',
        }
        
class ParentForm(forms.ModelForm):
    """ Creates a new parent. Requires parent to be user in parent group"""
    class Meta:
        model = Parent
        fields = ('parent_name', 'phone_number',)     

class TeacherForm(forms.ModelForm):
    """Creates a new teacher. Requires teacher to be in teacher group"""
    phone_number = forms.IntegerField(required=True) 
    class Meta:
        model = Teacher
        fields = ('teacher_name', 'phone_number',)

class GetregisterForm(forms.ModelForm):
    """Creates the filter to find students expected to be in a session"""
    class Meta:
        model = Timetable
        fields = ('day', 'session', 'subject_name')
             


# Form to do the register
class RegisterForm(forms.ModelForm):
    """Creates a form with the student name already in filled in"""
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

# Form to review pending absences.
class PendingabsenceForm(forms.ModelForm):
    class Meta:
        model = DailyRegister
        fields = ['status', 'code']
   

# Form to get the class list   
class GetclassForm(forms.Form):
    subject_name = forms.ModelChoiceField(
        queryset = Subject.objects.all(),
        empty_label="Choose a subject..",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
# Form to remove a student.
class RemoveForm(forms.Form):
    # Force the field to render as a ChoiceField dropdown
    student_code = forms.ModelChoiceField(
        queryset = Student.objects.filter(deregistered=False),
        widget = forms.Select(attrs={'class': 'form-control'}),
        label = "Select student to remove",
    )
        
        
        
        
    
    
        
    
        


        