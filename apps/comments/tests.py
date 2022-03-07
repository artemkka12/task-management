from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from apps.comments.models import Comment


class CommentTest(APITestCase):
    def test_access_token(self):
        username = "string"
        password = "stringstring"
        self.user = User.objects.create_user(username, username, password)
        jwt_fetch_data = {
            'username': username,
            'password': password
        }

        response = self.client.post('/user/token/', jwt_fetch_data, 'json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_task(self):
        self.test_access_token()
        data = {
            "title": "string",
            "description": "string",
            "completed": True
        }
        response = self.client.post('/task/tasks/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_post_comment(self):
        self.test_create_task()

        data = {
            "task": 1,
            "text": "string"
        }

        response = self.client.post('/comment/create-comment/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_json = response.json()
        task_id = response_json['task']
        comment = Comment.objects.get(pk=1)
        self.assertEqual(task_id, comment.task_id)