from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginTest(APITestCase):
    def setUp(self):  # Corrected the method name to 'setUp'
        """
        Set up a test user
        """
        self.user = User.objects.create_user(
            email='clint@mail.comgg',
            password='blindspot',
            first_name='Clinton',
            last_name='hn',
            role='hr_admin'
        )
        self.login_url = 'http://127.0.0.1:8000/api/auth/login/'

    def test_login_success(self):
        """
        Test successful login
        """
        response = self.client.post(self.login_url, {
            'email': 'clint@mail.comgg',
            'password': 'blindspot'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_failure_invalid_credentials(self):
        """
        Test login with invalid credentials
        """
        response = self.client.post(self.login_url, {
            'email': 'clint@mail.comgg',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
