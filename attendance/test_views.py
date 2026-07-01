import pytest
from django.contrib.auth.models import User, Group, AnonymousUser
from django.urls import reverse
from django.test import TestCase, RequestFactory
from .views import landing_router, LandingView
from .models import Student, Subject, Timetable, DailyRegister

class TestHomeview(TestCase):
    """Tests Homeview loads succesfully"""
    def test_homepage_status_code_and_template(self):
        """Checks page loads successfully and uses correct template"""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'attendance/home.html')

# Allow use of database.
@pytest.mark.django_db
class TestLandingrouter:
    """Tests Landing_router redirects users to the appropriate landing page"""
    # Allow all tests to use the setup_data
    @pytest.fixture(autouse=True)
    def setup_data(self):
        """Set up the parent and teacher groups"""
        self.factory = RequestFactory()
        self.teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.parent_group, _ = Group.objects.get_or_create(name='parent')
        self.user = User.objects.create(username='FlorenceFox', password='testpassword')
    def test_teacher_redirect(self):
        """Test teachers access the landing page."""
        self.user.groups.add(self.teacher_group)
        request = self.factory.get('/landing/')
        request.user = self.user
        response = landing_router(request)
        assert response is not None
        assert response.status_code == 200
    def test_parent_redirect(self):
        """Tests parents access the landing page"""
        self.user.groups.add(self.parent_group)
        request = self.factory.get('/landing/')
        request.user = self.user
        response = landing_router(request)
        assert response is not None
        assert response.status_code == 200
    def test_wrong_user(self):
        """Tests a user that is not a parent or a teacher gets redirected home"""
        request = self.factory.get('/landing')
        request.user = self.user
        response = landing_router(request)
        assert response.status_code == 302
        assert response. url == '/'

class TestLandingview(TestCase):
    """Tests LandingView. Requires user log in"""
    def setUp(self):
        """Sets up url and creates a user"""
        self.factory = RequestFactory()
        self.url = reverse('landing')
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.user = User.objects.create_user(username = 'MiriamGonzalez', password='mypassword')
        self.user.groups.add (teacher_group)
    def test_nonuser_is_redirected(self):
        """Tests a non user is directed to login page"""
        request = self.factory.get("/landing/")
        request.user = AnonymousUser()
        response = LandingView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))
    def test_user_gets_access(self):
        """ Tests a teacher user gets access to landing page"""
        login_successful = self.client.login(username='MiriamGonzalez', password='mypassword')
        self.assertTrue(login_successful, "Test failed")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "attendance/landing.html")

class TestChildrenlist(TestCase):
    """Tests that parents are directed to landing page"""
    def setUp(self):
        """
            Creates an instance of a parent user with a registered child and a degegistered child.
            Creates a different instance of a parent user with a differet child.
            Sets up url
            """
        self.test_user = User.objects.create_user(username="FrederikFox", password="mypassword")
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.test_user.groups.add (parent_group)
        self.test_child1 = Student.objects.create(student_code='0609PITE', date_of_birth="2006-09-12",sex=3, group=0,music_option=4, parent_name=self.test_user, deregistered=False)
        self.test_child2 = Student.objects.create(student_code='0609PIDE', date_of_birth="2006-09-12",sex=3, group=0,music_option=4, parent_name=self.test_user, deregistered=True) 
        self.test_user1 = User.objects.create_user(username="MidgePeterson", password="mypassword1")
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.test_user1.groups.add (parent_group)
        self.test_child3 = Student.objects.create(student_code='060PESR', date_of_birth="2006-09-12",sex=3, group=0,music_option=4, parent_name=self.test_user1, deregistered=False)
        self.url = reverse('landing')
    def test_unauthentificateduser_is_redirected(self):
        """Unauthenticated users cannot access the landing page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    def test_only_registered_children_on_list(self):
        """Tests only the registered children belonging to parent user appear on list"""
        self.client.login(username='FrederikFox', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "attendance/landing.html")
        children_in_context = response.context['children']
        self.assertIn(self.test_child1, children_in_context)
        self.assertNotIn(self.test_child2, children_in_context)
        self.assertNotIn(self.test_child3, children_in_context)
        
class TestStudentlist(TestCase):
    """Tests    """
    def setUp(self):
        """ 
        Sets up url.
        Sets up teacher user
        Sets up a registered and deregistered students (Require parent user)
        Sets up daily register records for registered student (Require teacher user, Timetable and Session instance)
        """
        self.url = reverse('students')
        # Teacher user
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(username = 'MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add (teacher_group)
        #Registered and deregistered students
        self.test_user = User.objects.create_user(username="FrederikFox", password="mypassword")
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.test_user.groups.add (parent_group)
        self.test_student1 = Student.objects.create(student_code='0609PITE', date_of_birth="2006-09-12",sex=3, group=0,music_option=4, parent_name=self.test_user, deregistered=False)
        self.test_student2 = Student.objects.create(student_code='0609PIDE', date_of_birth="2006-09-12",sex=3, group=0,music_option=4, parent_name=self.test_user, deregistered=True) 
        # DailyRegisters records for self.test_child1
        self.test_subject = Subject.objects.create(subject_name='Maths A', teacher_name=self.teacher_user, set=1, room=1)
        self.test_session = Timetable.objects.create(session_id=2, day=1, session=0, group=1, subject_name=self.test_subject)
        self.test_register1 = DailyRegister.objects.create(session_id=self.test_session, date='2026-06-16', student_code=self.test_student1, mark=1)
        self.test_register2 = DailyRegister.objects.create(session_id=self.test_session, date='2026-06-23', student_code=self.test_student1, mark=0)
        
    def test_unauthentificated_user_is_redirected(self):
        """Unauthenticated users cannot access the students page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    def test_registered_students_on_list(self):
        """
            Checks teacher users can access the page
            Checks only registered students appear on the list
            """
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "attendance/students_list.html")
        students_in_context = response.context['students']
        self.assertIn(self.test_student1, students_in_context)
        self.assertNotIn(self.test_student2, students_in_context)
     
class TestAddparent(TestCase):
   
    """Tests add_parent(). Requires user to be admissions_officer"""
    def setUp(self):
        """Creates teacher and admissions_officer users. Sets up url"""
        self.url =  reverse('newparent')
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(username = 'MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add (teacher_group)
        admissions_group, _ = Group.objects.get_or_create(name='admissions_officer')
        self.admissions_user = User.objects.create_user(username='Headmaster', password='whatnow24')
        self.admissions_user.groups.add(admissions_group)
    def test_non_user_rejected(self):
        """Tests non users have not access to the page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
    def test_user_wrong_group_rejected(self):
        """Tests a user that is not admissions_officer is rejected"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
    def test_admissions_officer_accepted(self):
        """Tests the admissions_officer user is accepted"""
        self.client.login(username='Headmaster', password='whatnow24')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    def test_successful_form_submission(self):
        """Tests validated form is submitted correctly"""
        post_data = {
            'username': "PeterSmith",
            'first_name': "Peter",
            'last_name': "Smith",
            'email': "peter@lucella.com",
            'password': "mypassword",
        }
        Group.objects.get_or_create(name='parent')
        self.client.login(username='Headmaster', password='whatnow24')
        response = self.client.post(reverse('newparent'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('parentdata'))
        
        
        
        
        
        
    