import pytest
from django.contrib.auth.models import User, Group, AnonymousUser
from django.urls import reverse
from django.test import TestCase, RequestFactory
from attendance.views import landing_router, LandingView

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
        login_successful = self.client.login(username='MiriamGonzalez', password='mypassword', backend='allauth.account.auth_backends.AuthenticationBackend')
        self.assertTrue(login_successful, "Test failed")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "attendance/landing.html")
        
        

        
    