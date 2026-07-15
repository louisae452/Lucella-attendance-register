from django import forms
from django.contrib.auth.models import User
from django.forms import modelformset_factory

from .models import (
    DailyRegister,
    Parent,
    Sentemail,
    Student,
    Subject,
    Teacher,
    Timetable,
)


class StudentForm(forms.ModelForm):
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
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)
        help_texts = {
            'username': 'The user name is the name followed '
            'by surname wihtout spaces',
        }


class ParentForm(forms.ModelForm):
    # AI generated code to only accept phone numbers on field
    phone_number = forms.RegexField(
        # Blocks text, allows only digits (9-15 long), accepts an optional '+'
        regex=r'^\+?1?\d{9,15}$',
        max_length=15,
        min_length=9,
        error_messages={
            'invalid': "Please enter a valid phone number. "
            "Letters and symbols (except +) are not allowed."
        },
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'placeholder': '+1234567890',
            #  HTML5 Pattern: Restricts input to only numbers and the '+' sign
            'pattern': r'^\+?\d+$',
            'title': 'Please enter a valid phone number containing '
            'only numbers (e.g., +1234567890).'
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
    # AI generated code to only accept phone numbers on field
    phone_number = forms.RegexField(
        # Blocks text, allows only digits (9-15 long), accepts an optional '+'
        regex=r'^\+?1?\d{9,15}$',
        max_length=15,
        min_length=9,
        error_messages={
            'invalid': "Please enter a valid phone number. "
            "Letters and symbols (except +) are not allowed."
        },
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'placeholder': '+1234567890',
            #  HTML5 Pattern: Restricts input to only numbers and the '+' sign
            'pattern': r'^\+?\d+$',
            'title': 'Please enter a valid phone number containing '
            'only numbers (e.g., +1234567890).'
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
    class Meta:
        model = Timetable
        fields = ('day', 'session', 'subject_name')
        widgets = {
            'day': forms.Select(attrs={'class': 'choicebox'}),
            'session': forms.Select(attrs={'class': 'choicebox'}),
            'subject_name': forms.Select(attrs={'class': 'choicebox'}),
        }


class RegisterForm(forms.ModelForm):
    class Meta:
        model = DailyRegister
        fields = ['student_code', 'mark']
        widgets = {
            'mark': forms.Select(attrs={'class': 'choicebox'}),
        }

    def __init__(self, *for_args, **kwargs):
        super().__init__(*for_args, **kwargs)
        self.fields['student_code'].disabled = True


# Ccreate formset class:
RegisterFormSet = modelformset_factory(
    DailyRegister, form=RegisterForm, extra=0)


class SendemailForm(forms.ModelForm):
    """cts an email to be sent"""
    class Meta:
        model = Sentemail
        fields = ['subject']
        widgets = {
            'subject': forms.Select(attrs={'class': 'choicebox'}),
        }


class AbsenceForm(forms.ModelForm):
    reason_for_absence = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = DailyRegister
        fields = ['date', 'reason_for_absence']
        help_texts = {
            'date': 'Please, use this format:<br> YYYY-MM-DD',
        }


class GivereasonForm(forms.ModelForm):
    reason_for_absence = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = DailyRegister
        fields = ['reason_for_absence']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if not instance or not instance.pk:
            raise ValueError("A valid instance is required")
        super().__init__(*args, **kwargs)


class PendingabsenceForm(forms.ModelForm):
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


class GetclassForm(forms.Form):
    subject_name = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        empty_label="Choose a subject..",
        widget=forms.Select(attrs={'class': 'form-control choicebox'})
    )


class RemoveForm(forms.Form):
    # Force the field to render as a ChoiceField dropdown
    student_code = forms.ModelChoiceField(
        queryset=Student.objects.filter(deregistered=False),
        widget=forms.Select(attrs={'class': 'choicebox'}),
        label="Select student to deregister",
    )
