from .models import Student, Parent, Teacher, Timetable, DailyRegister, Sentemail, Subject


from django import forms
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from django.contrib.auth.models import User

# Form to add a new student


class StudentForm(forms.ModelForm):
    """Form to add a new student.
    Requires parent to be a user with group parent"""
    class Meta:
        model = Student
        fields = ('student_name', 'student_surname', 'student_code',
                  'parent_name', 'date_of_birth', 'sex', 'group',
                  'music_option',)
        help_texts = {
            'student_code': 'The student code is the last two digits'
            'of the year of birth, month of birth, first two letters'
            'of surname followed by first two letters of name in capitals.',
        }
        widgets = {
            'parent_name': forms.Select(attrs={'class': 'choicebox'}),
            'sex': forms.Select(attrs={'class': 'choicebox'}),
            'group': forms.Select(attrs={'class': 'choicebox'}),
            'music_option': forms.Select(attrs={'class': 'choicebox'}),
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
    # AI generated code to only accept phone numbers on field
    phone_number = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',  # Blocks text, allows only digits (9-15 long), accepts an optional '+'
        max_length=15,
        min_length=9,
        error_messages={
            'invalid': "Please enter a valid phone number. Letters and symbols (except +) are not allowed."
        },
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'placeholder': '+1234567890',
            #  HTML5 Pattern: Restricts input to only numbers and the '+' sign
            'pattern': r'^\+?\d+$', 
            'title': 'Please enter a valid phone number containing only numbers (e.g., +1234567890).'
        })
    )
    # End of AI generated code
    class Meta:
        model = Parent
        fields = ('parent_name', 'phone_number',)
        widgets = {
            'parent_name': forms.Select(attrs={'class': 'choicebox'}),
            # Phone constraints. 
            
        }     

class TeacherForm(forms.ModelForm):
    """Creates a new teacher. Requires teacher to be in teacher group"""
    # AI generated code to only accept phone numbers on field
    phone_number = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',  # Blocks text, allows only digits (9-15 long), accepts an optional '+'
        max_length=15,
        min_length=9,
        error_messages={
            'invalid': "Please enter a valid phone number. Letters and symbols (except +) are not allowed."
        },
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'placeholder': '+1234567890',
            #  HTML5 Pattern: Restricts input to only numbers and the '+' sign
            'pattern': r'^\+?\d+$', 
            'title': 'Please enter a valid phone number containing only numbers (e.g., +1234567890).'
        })
    )
    # End of AI generated code
     
    class Meta:
        model = Teacher
        fields = ('teacher_name', 'phone_number',)
        widgets = {
            'teacher_name': forms.Select(attrs={'class': 'choicebox'}),
        }  

class GetregisterForm(forms.ModelForm):
    """Creates the filter to find students expected to be in a session"""
    class Meta:
        model = Timetable
        fields = ('day', 'session', 'subject_name')
        widgets = {
            'day': forms.Select(attrs={'class': 'choicebox'}),
            'session': forms.Select(attrs={'class': 'choicebox'}),
            'subject_name': forms.Select(attrs={'class': 'choicebox'}),
        }  
             


# Form to do the register
class RegisterForm(forms.ModelForm):
    """Creates a form with the student name already in filled in"""
    class Meta:
        model = DailyRegister
        fields=['student_code', 'mark']
        widgets = {
            'mark': forms.Select(attrs={'class': 'choicebox'}),
        }  
    def __init__(self, *for_args, **kwargs):
        super().__init__(*for_args, **kwargs)
        self.fields['student_code'].disabled = True
        
        
#create formset class:
RegisterFormSet = modelformset_factory(DailyRegister, form=RegisterForm, extra=0)    

# Create form to send email.
class SendemailForm(forms.ModelForm):
    "Selects an email to be sent"
    class Meta:
        model = Sentemail
        fields = ['subject']
        widgets = {
            'subject': forms.Select(attrs={'class': 'choicebox'}),
        }
        
        
# Form to register an absence.

class AbsenceForm(forms.ModelForm):
    """Creates a form to report an absence in the future"""
    reason_for_absence = forms.CharField( required=True, widget=forms.Textarea)
    class Meta:
        model = DailyRegister
        fields = ['date', 'reason_for_absence']
        help_texts = {
            'date': 'Please, use this format:<br> YYYY-MM-DD',
        }
# Form to give/edit reason for a past absence.
class GivereasonForm(forms.ModelForm):
    """Allows to update a past absence"""
    reason_for_absence = forms.CharField( required=True, widget=forms.Textarea)
    class Meta:
        model = DailyRegister
        fields = ['reason_for_absence']
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if not instance or not instance.pk:
            raise ValueError("A valid instance is required")
        super().__init__(*args, **kwargs)
        
# Form to review pending absences.
class PendingabsenceForm(forms.ModelForm):
    """Allows Attendance Officer to review absences"""
    class Meta:
        model = DailyRegister
        fields = ['status', 'code']
        widgets = {
            'status': forms.Select(attrs={'class': 'choicebox'}),
            'code': forms.Select(attrs={'class': 'choicebox'}),
        }
        
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if not instance or not instance.pk:
            raise ValueError("A valid instanceis required")
        super().__init__(*args, **kwargs)
        
   

# Form to get the class list   
class GetclassForm(forms.Form):
    """Allows teacher to select a subject"""
    subject_name = forms.ModelChoiceField(
        queryset = Subject.objects.all(),
        empty_label="Choose a subject..",
        widget=forms.Select(attrs={'class': 'form-control choicebox'})
    )
# Form to remove a student.
class RemoveForm(forms.Form):
    """Allows Admissions Officer to deregister a student"""
    # Force the field to render as a ChoiceField dropdown
    student_code = forms.ModelChoiceField(
        queryset = Student.objects.filter(deregistered=False),
        widget = forms.Select(attrs={'class': 'choicebox'}),
        label = "Select student to deregister",
    )
        
        
        
        
    
    
        
    
        


        