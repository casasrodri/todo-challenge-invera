from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from app.utils import get_date
from tasks.models import Task


class TaskIntegrationTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/tasks/"

        user = User.objects.create_user(username="rodri", password="rodri")

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        token = refresh.access_token

        # Set the token in the client auth headers
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def __create_task(self):
        return Task.objects.create(title="Task", description="This is a task")

    def test_create_task(self):
        data = {"title": "New task", "description": "This is a new task"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get(id=response.data["id"]).title, "New task")

    def test_get_task_list(self):
        for i in range(5):
            self.__create_task()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_get_task(self):
        task = self.__create_task()
        response = self.client.get(f"{self.url}{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], task.title)

    def test_update_task(self):
        task = self.__create_task()
        data = {"title": "Updated task", "complete": "True"}
        response = self.client.put(f"{self.url}{task.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Task.objects.get(id=task.id).complete)

    def test_delete_task(self):
        task = self.__create_task()
        response = self.client.delete(f"{self.url}{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_complete_task(self):
        task = self.__create_task()
        response = self.client.post(f"{self.url}{task.id}/complete/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Task.objects.get(id=task.id).complete)

    def test_filter_tasks(self):
        task = self.__create_task()
        response = self.client.get(f"{self.url}?description=this is a")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], task.title)

    def test_filter_tasks_date(self):
        # Task within the range
        task1 = self.__create_task()
        task1.created = get_date("2024-07-23")
        task1.save()

        # Task out of the range
        task2 = self.__create_task()
        task2.created = get_date("2024-01-02")
        task2.save()

        # Get taks within the range
        response = self.client.get(
            f"{self.url}?created_from=2024-07-01&created_to=2024-12-31"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
