import datetime
import time

from django.contrib.auth.models import User
from pytz import UTC
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase

from apps.tasks.models import Task, Timer, Timelog


class TaskTests(APITestCase):
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

    def test_get_all_tasks(self):
        self.test_access_token()

        data = {
            "title": "string",
            "description": "string",
            "completed": True
        }
        self.client.post('/task/tasks/', data, 'json')
        self.client.post('/task/tasks/', data, 'json')
        self.client.post('/task/tasks/', data, 'json')

        response = self.client.get('/task/tasks/', data={'format': 'json'})
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 3)

    def test_get_completed_tasks(self):
        self.test_access_token()

        data = {
            "title": "string",
            "description": "string",
            "completed": True
        }

        response = self.client.post('/task/tasks/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response = self.client.post('/task/tasks/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response = self.client.post('/task/tasks/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)

        response = self.client.get('/task/tasks/view_completed_tasks/', data={'format': 'json'})
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 3)

    def test_my_tasks(self):
        self.test_create_task()

        username = "string2"
        password = "stringstringstring"

        self.user = User.objects.create_user(username, username, password)

        jwt_fetch_data = {
            'username': username,
            'password': password
        }

        response = self.client.post('/user/token/', jwt_fetch_data, 'json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            "title": "string",
            "description": "string",
            "completed": True
        }
        response = self.client.post('/task/tasks/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)

        response = self.client.get('/task/tasks/view_my_tasks/', data={'format': 'json'})
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Task.objects.filter(owner__username='string').count(), 1)

    def test_task_detail(self):
        self.test_access_token()

        data = {
            "title": "string",
            "description": "string",
            "completed": False
        }

        response = self.client.post('/task/tasks/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)

        response = self.client.post('/task/tasks/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)

        response = self.client.get('/task/tasks/1/', data={'format': 'json'})
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_json = response.json()
        task_id = response_json.get('id')
        self.assertEqual(task_id, 1)

    def test_put_task(self):
        self.test_create_task()
        data = {
            "title": "stringstring",
            "description": "string",
            "completed": True
        }
        response = self.client.put('/task/tasks/1/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_json = response.json()
        title = response_json.get('title')
        self.assertEqual(title, 'stringstring')

    def test_patch_task(self):
        self.test_create_task()
        data = {
            "description": "stringstringstringstring",
        }
        response = self.client.patch('/task/tasks/1/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_json = response.json()
        description = response_json.get('description')
        self.assertEqual(description, 'stringstringstringstring')

    def test_delete_task(self):
        self.test_create_task()
        response = self.client.delete('/task/tasks/1/')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_assign_task_to_user(self):
        self.test_create_task()

        data = {
            "first_name": "string",
            "last_name": "string",
            "username": "string1",
            "email": "faer.faer.2006@mail.ru",
            "password": "string"
        }

        response = self.client.post('/user/register/', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        data = {
            'owner': 2
        }
        response = self.client.patch('/task/tasks/1/assign_task_to_user/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_json = response.json()
        owner = response_json.get('owner')
        self.assertEqual(owner, 2)

    def test_complete_task(self):
        self.test_access_token()

        data = {
            "title": "stringstring",
            "description": "string",
            "completed": False
        }

        response = self.client.post('/task/tasks/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_json = response.json()
        completed = response_json.get('completed')
        self.assertEqual(completed, False)

        response = self.client.patch('/task/tasks/1/complete_task/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        task = Task.objects.get(id=1)
        self.assertEqual(task.completed, True)

    def test_time_log(self):
        self.test_create_task()

        """Start timer"""

        response = self.client.post('/task/tasks/1/start_time_log/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        timer = Timer.objects.filter(task_id=1, owner_id=1).last()
        self.assertEqual(timer.is_stopped, False)
        self.assertEqual(timer.is_running, True)

        time.sleep(5)

        """Pause timer"""

        response = self.client.post('/task/tasks/1/pause_time_log/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        timer = Timer.objects.filter(task_id=1, owner_id=1).last()
        self.assertEqual(timer.is_stopped, False)
        self.assertEqual(timer.is_running, False)

        """Start timer again"""

        response = self.client.post('/task/tasks/1/start_time_log/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        timer = Timer.objects.filter(task_id=1, owner_id=1).last()
        self.assertEqual(timer.is_stopped, False)
        self.assertEqual(timer.is_running, True)

        time.sleep(3)

        response = self.client.post('/task/tasks/1/stop_time_log/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        timer = Timer.objects.filter(task_id=1, owner_id=1).last()
        self.assertEqual(timer.is_stopped, True)
        self.assertEqual(timer.is_running, False)
        timelog = Timelog.objects.all()
        self.assertEqual(timelog.count(), 2)

    def test_manual_time_log(self):
        self.test_create_task()

        data = {
            "started_at": "2022-03-01T12:34:05.705Z",
            "duration": 2
        }

        response = self.client.post('/task/tasks/1/manual_time_log/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        timelog = Timelog.objects.filter(task_id=1, owner_id=1).last()
        self.assertEqual(timelog.duration, datetime.timedelta(seconds=2))
        self.assertEqual(timelog.started_at, datetime.datetime(2022, 3, 1, 12, 34, 5, 705000, tzinfo=UTC))
        self.assertEqual(timelog.stopped_at, datetime.datetime(2022, 3, 1, 12, 34, 5, 705000, tzinfo=UTC)
                         + datetime.timedelta(seconds=2))

    def test_time_spent_by_task(self):
        self.test_time_log()

        response = self.client.get('/task/tasks/1/time_spent_by_task/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_amount_logged_time(self):
        self.test_time_log()

        response = self.client.get('/task/tasks/amount_by_last_month/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_top_task_by_last_month(self):
        self.test_time_log()

        data = {
            "title": "string",
            "description": "string",
            "completed": True
        }
        response = self.client.post('/task/tasks/', data, 'json')
        self.assertEqual(response.status_code, HTTP_200_OK)

        response = self.client.post('/task/tasks/2/start_time_log/')
        self.assertEqual(response.status_code, HTTP_200_OK)

        time.sleep(8)

        response = self.client.post('/task/tasks/2/pause_time_log/')
        self.assertEqual(response.status_code, HTTP_200_OK)

        response = self.client.post('/task/tasks/2/start_time_log/')
        self.assertEqual(response.status_code, HTTP_200_OK)

        time.sleep(1)

        response = self.client.post('/task/tasks/2/stop_time_log/')
        self.assertEqual(response.status_code, HTTP_200_OK)

        response = self.client.get('/task/tasks/top_tasks_by_last_month/')
        self.assertEqual(response.status_code, HTTP_200_OK)