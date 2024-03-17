from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Project, Task

User = get_user_model()


class ProjectModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@localhost", password="testpass"
        )

    def test_project_creation(self):
        project = Project.objects.create(name="Test Project", owner=self.user)
        self.assertEqual(str(project), "Test Project")


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@localhost", password="testpass"
        )
        self.project = Project.objects.create(name="Test Project", owner=self.user)

    def test_task_creation(self):
        task = Task.objects.create(
            name="Test Task",
            description="Test description",
            due_date="2023-05-01",
            priority="high",
            owner=self.user,
            project=self.project,
        )
        self.assertEqual(str(task), "Test Task")
