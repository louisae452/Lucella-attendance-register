from django.test import TestCase
from django.contrib.auth.models import Group as AuthGroup, User

from .models import Subject
from .forms import StudentForm, UserForm, ParentForm, TeacherForm, GetregisterForm

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
               

        
        
        
       
    
    