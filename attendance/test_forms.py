from django.test import TestCase
from django.contrib.auth.models import Group as AuthGroup, User
from django.contrib.auth import get_user_model
from .models import Parent

from .forms import StudentForm

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
        
       
    
    