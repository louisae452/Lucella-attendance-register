import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.test import TestCase, RequestFactory
from attendance.views import landing_router

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
        

        
    