from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.cache import cache

class UserCreateTests(APITestCase):

    def test_create_user_success(self):
        """
        Ensure we can create a new user with valid data.
        """
        url = reverse('create_user')
        data = {
            'username': 'newuser',
            'password': 'SecurePass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])

    def test_create_user_invalid_password(self):
        """
        Ensure we cannot create a user with an invalid password.
        """
        url = reverse('create_user')
        data = {
            'username': 'newuser',
            'password': 'short'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('reason', response.data)

    def test_create_user_duplicate_username(self):
        """
        Ensure we cannot create a user with a duplicate username.
        """
        User.objects.create_user(username='newuser', password='SecurePass123')
        url = reverse('create_user')
        data = {
            'username': 'newuser',
            'password': 'SecurePass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('reason', response.data)


class LoginViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='SecurePass123')
    
    def tearDown(self):
        cache.clear()

    def test_login_success(self):
        """
        Ensure we can login with valid credentials.
        """
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'SecurePass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_invalid_credentials(self):
        """
        Ensure we cannot login with invalid credentials.
        """
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'WrongPassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('reason', response.data)

    def test_login_too_many_attempts(self):
        """
        Ensure the login is blocked after too many failed attempts.
        """
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'WrongPassword'
        }
        for _ in range(5):
            self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('reason', response.data)

