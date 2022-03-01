from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def test_user_register(self):
        data = {
          "first_name": "string",
          "last_name": "string",
          "username": "string",
          "email": "faer.faer.2006@mail.ru",
          "password": "string"
        }

        response = self.client.post('/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
          "first_name": "string",
          "last_name": "string",
          "username": "string1",
          "email": "faer.faer.2006@mail.ru",
          "password": "string"
        }

        response = self.client.post('/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_access_token(self):
        """Create a user"""

        username = "string"
        password = "stringstring"
        self.user = User.objects.create_user(username, username, password)
        jwt_fetch_data = {
            'username': username,
            'password': password
        }

        response = self.client.post('/user/token/', jwt_fetch_data, 'json')

        """Test access token"""

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        """Test refresh token"""

        self.refresh_token = response.data['refresh']

        data = {
            'refresh': self.refresh_token
        }
        response = self.client.post('/user/token/refresh/', data, 'json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_get_all_users(self):
        response = self.client.get('/user/users-list/', data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
