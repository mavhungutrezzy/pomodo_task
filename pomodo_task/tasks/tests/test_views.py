from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Project, Task

User = get_user_model()


class ProjectViewSetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@localhost", password="testpass"
        )
        self.client.login(email="test@localhost", password="testpass")

    def test_create_project(self):
        url = reverse("project-list")
        data = {"name": "Test Project", "description": "Test description"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)


class TaskViewSetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@localhost", password="testpass"
        )
        self.client.login(email="test@localhost", password="testpass")
        self.project = Project.objects.create(name="Test Project", owner=self.user)

    def test_create_task(self):
        url = reverse("task-list")
        data = {
            "name": "Test Task",
            "description": "Test description",
            "due_date": "2023-05-01",
            "priority": "high",
            "project": self.project.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
