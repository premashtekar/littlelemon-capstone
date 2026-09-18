from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationAndAuthTests(APITestCase):
    def test_user_can_register(self):
        response = self.client.post('/auth/users/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass123',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registered_user_can_obtain_token(self):
        User.objects.create_user(username='newuser', password='StrongPass123')
        response = self.client.post('/auth/token/login/', {
            'username': 'newuser',
            'password': 'StrongPass123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)
