from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.cache import cache

class UserCreateTests(APITestCase):

    def test_register_success(self):
        """
        Positive: register with valid data
        """
        url = reverse('create_user')
        data = {
            'username': 'yourusername1',
            'password': 'Youpassword1',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])

    def test_register_invalid_username(self):
        """
        Negative: register with invalid username
        """
        url = reverse('create_user')
        data_list = [
            {
            'username': 'y1',
            'password': 'Youpassword1',
            },
            {
            'username': 'yourusername1yourusername1yourusername1',
            'password': 'Youpassword1',
            },
        ]
        for data in data_list:
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertFalse(response.data['success'])
            self.assertIn('reason', response.data)

    def test_register_invalid_password(self):
        """
        Negative: register with invalid password
        """
        url = reverse('create_user')
        data_list = [
            {
            'username': 'yourusername1',
            'password': 'Youpa1',
            },
            {
            'username': 'yourusername1',
            'password': 'Youpassword1Youpassword1Youpassword1',
            },
            {
            'username': 'yourusername1',
            'password': 'youpassword1',
            },
            {
            'username': 'yourusername1',
            'password': 'Youpassword',
            },
        ]
        for data in data_list:
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertFalse(response.data['success'])
            self.assertIn('reason', response.data)

    def test_create_user_duplicate_username(self):
        """
        Negative: duplicate username.
        """
        User.objects.create_user(username='yourusername1', password='Youpassword1')
        url = reverse('create_user')
        data = {
            'username': 'yourusername1',
            'password': 'Youpassword1',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('reason', response.data)


class LoginViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='yourusername1', password='Youpassword1')
    
    def tearDown(self):
        cache.clear()

    def test_login_success(self):
        """
        Positive: login with valid credentials.
        """
        url = reverse('login')
        data = {
            'username': 'yourusername1',
            'password': 'Youpassword1',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_invalid_credentials(self):
        """
        Negative: login with invalid credentials.
        """
        url = reverse('login')
        data = {
            'username': 'yourusername1',
            'password': 'Wrongpassword1',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('reason', response.data)

    def test_login_too_many_attempts(self):
        """
        the login is blocked after too many failed attempts.
        """
        url = reverse('login')
        data = {
            'username': 'yourusername1',
            'password': 'Wrongpassword1',
        }
        for _ in range(5):
            self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('reason', response.data)

