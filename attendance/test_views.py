from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

class TestHomeview(TestCase):
    """Tests Homeview loads succesfully"""
    def test_homepage_status_code_and_template(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'attendance/home.html')
    