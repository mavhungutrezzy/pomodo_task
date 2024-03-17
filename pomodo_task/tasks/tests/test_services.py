from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Project
from ..services import ProjectService, TaskService

User = get_user_model()


class ProjectServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@localhost", password="testpass"
        )

    def test_create_project(self):
        project = ProjectService.create_project(
            self.user, "Test Project", "Test description"
        )
        self.assertEqual(project.name, "Test Project")


class TaskServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@localhost", password="testpass"
        )
        self.project = Project.objects.create(name="Test Project", owner=self.user)

    def test_create_task(self):
        task = TaskService.create_task(
            self.user,
            "Test Task",
            "Test description",
            "2023-05-01",
            "high",
            self.project,
        )
        self.assertEqual(task.name, "Test Task")
