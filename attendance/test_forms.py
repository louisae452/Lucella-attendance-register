from django.test import TestCase
from django.contrib.auth.models import Group as AuthGroup, User

from .models import Subject, Student, Email, DailyRegister, Timetable
from .forms import StudentForm, UserForm, ParentForm, TeacherForm, GetregisterForm, RegisterForm, SendemailForm, AbsenceForm, GivereasonForm, PendingabsenceForm, GetclassForm, RemoveForm

# Create your tests here.

class TestStudentForm(TestCase):
    """ Tests the StudentForm used to add a new student."""
    def setUp(self):
        """Creates a parent user."""
        # Create a parent group. (with help form AI)
        parent_group, _ = AuthGroup.objects.get_or_create(name='parent')
        # Create a user.
        self.test_user = User. objects.create(username='FlorenceFox', password='testpassword')
        # Assign user to parent group
        self.test_user.groups.add (parent_group)
        
    def test_form_is_valid(self):
        """ Tests the form is validated when all fields are filled in correctly."""
        data = {
            'student_name': 'Peter',
            'student_surname': 'Smith',
            'student_code':'0605SMPE',
            'parent_name':self.test_user.id, 
            'date_of_birth':'2006-05-14', 
            'sex':'3',
            'group': '1', 
            'music_option':'4'
            }
        student_form = StudentForm(data)
        if not student_form.is_valid():
            print("\nForm Errors:", student_form.errors.as_json())
        self.assertTrue(student_form.is_valid())
    def test_is_not_valid_name(self):
        """Tests form is not validated when Student_name is not filled in"""
        data = {
            'student_name': '',
            'student_surname': 'Smith',
            'student_code':'0605SMPE',
            'parent_name':self.test_user.id, 
            'date_of_birth':'2006-05-14', 
            'sex':'3',
            'group': '1', 
            'music_option':'4'
            }
        student_form = StudentForm(data)
        self.assertFalse(student_form.is_valid())
    def test_is_not_valid_surname(self):
        """Tests form is not validated when student_surname is not filled in"""
        data = {
            'student_name': 'Peter',
            'student_surname': '',
            'student_code':'0605SMPE',
            'parent_name':self.test_user.id, 
            'date_of_birth':'2006-05-14', 
            'sex':'3',
            'group': '1', 
            'music_option':'4'
            }
        student_form = StudentForm(data)
        if not student_form.is_valid():
            print("\nForm Errors:", student_form.errors.as_json())
        self.assertFalse(student_form.is_valid())
    def test_is_not_valid_code(self):
        """Tests form is not validated when student_code is not filled in"""
        data = {
            'student_name': 'Peter',
            'student_surname': 'Smith',
            'student_code':'',
            'parent_name':self.test_user.id, 
            'date_of_birth':'2006-05-14', 
            'sex':'3',
            'group': '1', 
            'music_option':'4'
            }
        student_form = StudentForm(data)
        if not student_form.is_valid():
            print("\nForm Errors:", student_form.errors.as_json())
        self.assertFalse(student_form.is_valid())
    def test_is_not_valid_parent(self):
        """Tests form is not validated when parent_name is not a parent user"""
        data = {
            'student_name': 'Peter',
            'student_surname': 'Smith',
            'student_code':'0605SMPE',
            'parent_name':'John Smith', 
            'date_of_birth':'2006-05-14', 
            'sex':'3',
            'group': '1', 
            'music_option':'4'
            }
        student_form = StudentForm(data)
        if not student_form.is_valid():
            print("\nForm Errors:", student_form.errors.as_json())
        self.assertFalse(student_form.is_valid())
    def test_is_not_valid_date(self):
        """Tests form is not validated when date_of_birth_ is not correct"""
        data = {
            'student_name': 'Peter',
            'student_surname': 'Smith',
            'student_code':'0605SMPE',
            'parent_name':self.test_user.id, 
            'date_of_birth':'14-04-2026', 
            'sex':'3',
            'group': '1', 
            'music_option':'4'
            }
        student_form = StudentForm(data)
        if not student_form.is_valid():
            print("\nForm Errors:", student_form.errors.as_json())
        self.assertFalse(student_form.is_valid())
    def test_is_not_valid_sex(self):
        """Tests form is not validated when sex option is not correct"""
        data = {
            'student_name': 'Peter',
            'student_surname': 'Smith',
            'student_code':'0605SMPE',
            'parent_name':self.test_user.id, 
            'date_of_birth':'2006-05-14', 
            'sex':'1',
            'group': '1', 
            'music_option':'4'
            }
        student_form = StudentForm(data)
        if not student_form.is_valid():
            print("\nForm Errors:", student_form.errors.as_json())
        self.assertFalse(student_form.is_valid())
    def test_is_not_valid_group(self):
        """ Tests form is not validated when group option is not correct""" 
        data = {
            'student_name': 'Peter',
            'student_surname': 'Smith',
            'student_code':'0605SMPE',
            'parent_name':self.test_user.id, 
            'date_of_birth':'2006-05-14', 
            'sex':'3', 
            'group': '3', 
            'music_option':'4'
            }
        student_form = StudentForm(data)
        if not student_form.is_valid():
            print("\nForm Errors:", student_form.errors.as_json())
        self.assertFalse(student_form.is_valid())
    def test_is_not_valid_music(self):
        """ Tests form is not validated when music_option is not correct"""
        data = {
            'student_name': 'Peter',
            'student_surname': 'Smith',
            'student_code':'0605SMPE',
            'parent_name':self.test_user.id, 
            'date_of_birth':'2006-05-14', 
            'sex':'3',
            'group': '1', 
            'music_option':'0'
            }
        student_form = StudentForm(data)
        if not student_form.is_valid():
            print("\nForm Errors:", student_form.errors.as_json())
        self.assertFalse(student_form.is_valid())

class TestUserForm(TestCase):
    """ Tests the UserForm used to add new users"""
    def test_is_valid(self):
        """Tests form is validated if all fields completed"""
        data = {
            'username': "PeterSmith",
            'first_name': "Peter",
            'last_name': "Smith",
            'email': "peter@lucella.com",
            'password': "mypassword",
        }
        user_form = UserForm(data)
        self.assertTrue(user_form.is_valid())
    def test_is_not_valid_username(self):
        """Tests form is not validated if there is not a username"""
        data = {
            'username': "",
            'first_name': "Peter",
            'last_name': "Smith",
            'email': "peter@lucella.com",
            'password': "mypassword",
        }
        user_form = UserForm(data)
        self.assertFalse(user_form.is_valid())
        
    def test_is_not_valid_name(self):
        """Tests form is not validated if there is not a name"""
        data = {
            'username': "PeterSmith",
            'first_name': "",
            'last_name': "Smith",
            'email': "peter@lucella.com",
            'password': "mypassword",
        }
        user_form = UserForm(data)
        self.assertFalse(user_form.is_valid())
        
    def test_is_not_valid_surname(self):
        """Tests form is not validated if there is not a surname"""
        data = {
            'username': "PeterSmith",
            'first_name': "Peter",
            'last_name': "",
            'email': "peter@lucella.com",
            'password': "mypassword",
        }
        user_form = UserForm(data)
        self.assertFalse(user_form.is_valid())
        
    def test_is_not_valid_email(self):
        """Tests form is not validated if there is no email"""
        data = {
            'username': "PeterSmith",
            'first_name': "Peter",
            'last_name': "Smith",
            'email': "",
            'password': "mypassword",
        }
        user_form = UserForm(data)
        self.assertFalse(user_form.is_valid())
        
    def test_is_not_valid_password(self):
        """Tests form is not validated if there is not a password"""
        data = {
            'username': "PeterSmith",
            'first_name': "Peter",
            'last_name': "Smith",
            'email': "peter@lucella.com",
            'password': "",
        }
        user_form = UserForm(data)
        self.assertFalse(user_form.is_valid())
        
class TestParentForm(TestCase):
    """Tests ParentForm. Requires parent to be a user in group parent"""
    def setUp(self):
        """Creates a parent user."""
        parent_group, _ = AuthGroup.objects.get_or_create(name='parent')
        self.test_user = User. objects.create(username='FlorenceFox', password='testpassword')
        self.test_user.groups.add (parent_group)
    def test_form_is_valid(self):
        """Tests ParentForm is validated if all fields completed correctly"""
        data = {
            'parent_name': self.test_user,
            'phone_number': '0987857473'
        }
        parent_form = ParentForm(data)
        self.assertTrue(parent_form.is_valid())
    def test_form_is_not_validated_name(self):
        """Tests ParentForm is not validated if parent_name is not a user in group parent"""
        data = {
            'parent_name': 'MiriamGonzalez',
            'phone_number': '0987857473'
        }
        parent_form = ParentForm(data)
        self.assertFalse(parent_form.is_valid())
    def test_form_is_not_validated_phone(self):
        """Tests ParentForm is not validated if parent_phone is not correct"""
        data = {
            'parent_name': self.test_user,
            'phone_number': ''
        }
        parent_form = ParentForm(data)
        self.assertFalse(parent_form.is_valid()) 

class TestTeacherForm(TestCase):
    """Tests TeacherForm. Requires teacher to be a user in group teacher"""
    def setUp(self):
        """Creates a teacher user."""
        teacher_group, _ = AuthGroup.objects.get_or_create(name='teacher')
        self.test_user = User. objects.create(username='MargaretMillicent', password='testpassword')
        self.test_user.groups.add (teacher_group)
    def test_form_is_valid(self):
        """Tests TeadchrForm is validated if all fields completed correctly"""
        data = {
            'teacher_name': self.test_user,
            'phone_number': '0987857473'
        }
        teacher_form = TeacherForm(data)
        self.assertTrue(teacher_form.is_valid())
    def test_form_is_not_validated_name(self):
        """Tests TesacherForm is not validated if teacher_name is not a user in group teacher"""
        data = {
            'teacher_name': 'MiriamGonzalez',
            'phone_number': '0987857473'
        }
        teacher_form = TeacherForm(data)
        self.assertFalse(teacher_form.is_valid())
    def test_form_is_not_validated_phone(self):
        """Tests TeacherForm is not validated if teacher_phone is not correct"""
        data = {
            'teacher_name': self.test_user,
            'phone_number': ''
        }
        teacher_form = TeacherForm(data)
        self.assertFalse(teacher_form.is_valid()) 

class TestGetregisterForm(TestCase):
    """Test GetregisterForm"""
    def setUp(self):
        """Creates a teacher user and a subject instance"""
        teacher_group, _ = AuthGroup.objects.get_or_create(name='teacher')
        self.test_user = User. objects.create(username='MargaretMillicent', password='testpassword')
        self.test_user.groups.add (teacher_group)
        self.test_subject = Subject.objects.create(subject_name='Maths A', teacher_name=self.test_user, set=1, room=1)
    def test_form_is_valid(self):
        """Tests GetregisterForm is validated if fields filled correctly"""
        data = {
            'day': 0,
            'session': 0,
            'subject_name': self.test_subject.pk,   
        }
        getregister_form = GetregisterForm(data)
        self.assertTrue(getregister_form.is_valid())
    def test_form_is_not_valid_day(self):
        """Tests GetregisterForm is not validated if day is not correct"""
        data = {
            'day': 7,
            'session': 0,
            'subject_name': self.test_subject.pk,   
        }
        getregister_form = GetregisterForm(data)
        self.assertFalse(getregister_form.is_valid())
    def test_form_is_not_valid_session(self):
        """Tests GetregisterForm is not validated if session is not correct"""
        data = {
            'day': 0,
            'session': 4,
            'subject_name': self.test_subject.pk,   
        }
        getregister_form = GetregisterForm(data)
        self.assertFalse(getregister_form.is_valid())
    def test_form_is_not_valid_subject(self):
        """Tests GetregisterForm is not validated if subject_name is not correct"""
        data = {
            'day': 0,
            'session': 0,
            'subject_name': "",   
        }
        getregister_form = GetregisterForm(data)
        self.assertFalse(getregister_form.is_valid())

class TestRegisterForm(TestCase):
    """Tests RegisterForm""" 
    def test_student_code_is_disabled(self):
        """Tests that student_code is disabled on initialisation"""
        register_form = RegisterForm()
        self.assertTrue(register_form.fields['student_code'].disabled)
    def setUp(self):
        """Creates a student instance. Requires parent instance"""
        parent_group, _  = AuthGroup.objects.get_or_create(name='parent')
        self.test_user = User. objects.create(username='FlorenceFox', password='testpassword')
        self.test_user.groups.add (parent_group)
        self.test_student = Student.objects.create(student_code='0609PITE', date_of_birth="2006-09-12",sex=3, group=0,music_option=4, parent_name=self.test_user)
    def test_form_is_valid(self):
        """Test RegisterForm is validated if data entered correctly"""
        data = {
            'mark': 1,
        }
        initial_data = {
            'student_code': self.test_student.pk,
        }
        register_form = RegisterForm(data, initial=initial_data)
        self.assertTrue(register_form.is_valid())
    def test_form_is_not_valid_code(self):
        """Tests RegisterForm is not validated if student_code is not initial value"""
        data = {
            'student_code': self.test_student.pk,
            'mark': 1,
        }
        register_form = RegisterForm(data)
        self.assertFalse(register_form.is_valid())
    def test_form_is_not_valid_mark(self):
        """Tests RegisterForm is not validated if mark in not filled correctly"""               
        data = {
            'mark': 5,
        }
        initial_data = {
            'student_code': self.test_student.pk,
        }
        register_form = RegisterForm(data, initial=initial_data)
        self.assertFalse(register_form.is_valid())
        
class TestSendemailForm(TestCase):
    """Tests SendemailForm"""
    def setUp(self):
        """Creates an email instance"""
        self.test_email = Email.objects.create(subject=2, text="Hello")
    def test_form_is_valid(self):
        """Tests SendemailForm is validated if data entered correctly"""
        data = {
            'subject': self.test_email,
        }
        sendemail_form = SendemailForm(data)
        self.assertTrue(sendemail_form.is_valid()) 
    def test_form_is_not_valid_subject(self):
        """Tests SendemailForm is not validated if subject is not correct"""
        data = {
            'subject': 'Good morning',
        }
        sendemail_form = SendemailForm(data)
        self.assertFalse(sendemail_form.is_valid())

class TestAbsenceForm(TestCase):
    """Tests AbsenceForm"""
    def test_form_is_valid(self):
        """Tests AbsenceForm is validated if data entered correctly"""
        data = {
            'date': '2026-07-19',
            'reason_for_absence': 'Not in',
        }  
        absence_form = AbsenceForm(data)
        self.assertTrue(absence_form.is_valid())
    def test_fom_is_not_valid_date(self):
        """Tests AbsenceForm is not validated if the date is not entered in the correct format"""
        data = {
            'date': '19-04-2026',
            'reason_for_absence': 'Not in',
        }  
        absence_form = AbsenceForm(data)
        self.assertFalse(absence_form.is_valid())
    def test_form_is_not_valid_reason(self):
        """Tests AbsenceForm is not validated if a reason is not entered"""
        data = {
            'date': '2026-07-19',
            'reason_for_absence': '',
        }  
        absence_form = AbsenceForm(data)
        self.assertFalse(absence_form.is_valid())

class TestGivereasonForm(TestCase):
    """Tests GivereasonForm. Requires DailyRegister instance"""
    def setUp(self):
        """Creates student, teacher, subject, timetable aned dailyregister instances."""
        parent_group, _ = AuthGroup.objects.get_or_create(name='parent')
        self.test_user = User. objects.create(username='FlorenceFox', password='testpassword')
        self.test_user.groups.add (parent_group)
        self.test_student = Student.objects.create(student_code='0609PITE', date_of_birth="2006-09-12",sex=3, group=0,music_option=4, parent_name=self.test_user)
        teacher_group, _ = AuthGroup.objects.get_or_create(name='teacher')
        self.test_teacheruser = User. objects.create(username='MargaretMillicent', password='testpassword')
        self.test_teacheruser.groups.add (teacher_group)
        self.test_subject = Subject.objects.create(subject_name='Maths A', teacher_name=self.test_teacheruser, set=1, room=1)
        self.test_session = Timetable.objects.create(session_id=2, day=1, session=0, group=1, subject_name=self.test_subject)
        self.test_register = DailyRegister.objects.create(session_id=self.test_session, date='2026-06-16', student_code=self.test_student)
    def test_form_is_valid(self):
        """Tests GivereasonForm is validated when field is filled correctly"""
        data = {
            'reason_for_absence': 'Not in'
        }
        givereason_form = GivereasonForm(data, instance=self.test_register)
        self.assertTrue(givereason_form.is_valid())
    def test_form_is_not_valid_instance(self):
        """Tests GivereasonForm is not validated if an instance is not provided"""
        data = {
            'reason_for_absence': 'Not in'
        }
        with self.assertRaises(ValueError):
            GivereasonForm(data)    
    def test_form_is_not_valid_reason(self):
        """Tests GivereasonForm is not valSidated when field is left empty"""
        data = {
            'reason_for_absence': ''
        }
        givereason_form = GivereasonForm(data, instance=self.test_register)
        self.assertFalse(givereason_form.is_valid())
        
class TestPendingabsenceForm(TestCase):
    """Tests PendingabsenceForm . Requires Dailyregister instance"""
    def setUp(self):
        """Creates student, teacher, subject, timetable and dailyregister instances."""
        parent_group, _ = AuthGroup.objects.get_or_create(name='parent')
        self.test_user = User. objects.create(username='FlorenceFox', password='testpassword')
        self.test_user.groups.add (parent_group)
        self.test_student = Student.objects.create(student_code='0609PITE', date_of_birth="2006-09-12",sex=3, group=0,music_option=4, parent_name=self.test_user)
        teacher_group, _ = AuthGroup.objects.get_or_create(name='teacher')
        self.test_teacheruser = User. objects.create(username='MargaretMillicent', password='testpassword')
        self.test_teacheruser.groups.add (teacher_group)
        self.test_subject = Subject.objects.create(subject_name='Maths A', teacher_name=self.test_teacheruser, set=1, room=1)
        self.test_session = Timetable.objects.create(session_id=2, day=1, session=0, group=1, subject_name=self.test_subject)
        self.test_register = DailyRegister.objects.create(session_id=self.test_session, date='2026-06-16', student_code=self.test_student)
    def test_form_is_valid(self):
        """Tests PendingabsenceForm is validated if form is filled correctly"""
        data = {
            'status': 1,
            'code': 0,
        }
        pendingabsence_form = PendingabsenceForm(data, instance=self.test_register)
        self.assertTrue(pendingabsence_form.is_valid())
    def test_form_is_not_valid_instance(self):
        """Tests PendingabsenceForm is not validated if an instance is not provided"""
        data = {
            'status': 1,
            'code': 0,
        }
        with self.assertRaises(ValueError):
            PendingabsenceForm(data)
    def test_form_is_not_valid_status(self):
        """Tests PendingabsenceForm is not validated if status is not provided"""
        data = {
            'status': '5',
            'code': 0,
        }
        pendingabsence_form = PendingabsenceForm(data, instance=self.test_register)
        self.assertFalse(pendingabsence_form.is_valid())
    def test_form_is_not_valid_code(self):
        """Tests PendingabsenceForm is not validated if code is not provided"""
        data = {
            'status': 1,
            'code': '6',
        }
        pendingabsence_form = PendingabsenceForm(data, instance=self.test_register)
        self.assertFalse(pendingabsence_form.is_valid())
        
class TestGetclassForm(TestCase):
    """Tests GetclassForm (requires subject instance)"""
    def setUp(self):
        """Creates an instance of teacher and subject"""
        teacher_group, _ = AuthGroup.objects.get_or_create(name='teacher')
        self.test_teacheruser = User. objects.create(username='MargaretMillicent', password='testpassword')
        self.test_teacheruser.groups.add (teacher_group)
        self.test_subject = Subject.objects.create(subject_name='Maths A', teacher_name=self.test_teacheruser, set=1, room=1)
    def test_form_is_valid(self):
        """Tests GetclassForm is validated when a valid instance is selected"""
        data = {
            'subject_name': self.test_subject,
        }
        getclass_form = GetclassForm(data)
        self.assertTrue(getclass_form.is_valid())
    def test_form_is_not_valid(self):
        """Tests GetclassForm is not validated when an invalid instance is enterered"""
        data = {
            'subject_name': "",
        }
        getclass_form = GetclassForm(data)
        self.assertFalse(getclass_form.is_valid())
        
class TestRemoveForm(TestCase):
    """Tests RemoveForm. Requires instance of registered and deregistered studetns."""
    def setUp(self):
        """Creates instances of registered and deregisterd students. Requires parent."""
        parent_group, _ = AuthGroup.objects.get_or_create(name='parent')
        self.test_user = User. objects.create(username='FlorenceFox', password='testpassword')
        self.test_user.groups.add (parent_group)
        self.test_student1 = Student.objects.create(student_code='0609PITE', date_of_birth="2006-09-12",sex=3, group=0,music_option=4, parent_name=self.test_user, deregistered=True)
        self.test_student2 = Student.objects.create(student_code='0609PICE', date_of_birth="2006-09-12",sex=3, group=0,music_option=4, parent_name=self.test_user, deregistered=False)
    def test_queriset_excludes_dergistered(self):
        """Checks that deregistered students are not on queryset""" 
        remove_form = RemoveForm()
        queryset = remove_form.fields['student_code'].queryset
        self.assertIn(self.test_student2, queryset)
        self.assertNotIn(self.test_student1, queryset)
    def test_form_is_valid(self):
        """Tests RemoveForm is validated when a registered student selected"""
        data = {
            'student_code': self.test_student2,
        }
        remove_form = RemoveForm(data)
        self.assertTrue(remove_form.is_valid())
    def test_form_is_not_valid(self):
        """Tests RemoveForm is not validated when a deregistered student selected"""
        data = {
            'student_code': self.test_student1,
        }
        remove_form = RemoveForm(data)
        self.assertFalse(remove_form.is_valid())
    
        
        
              
        
        
