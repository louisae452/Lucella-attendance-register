import pytest
from django.contrib.auth.models import User, Group, AnonymousUser
from django.urls import reverse
from django.test import TestCase, RequestFactory
from .views import landing_router, LandingView
from .models import Student

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
        
        
    