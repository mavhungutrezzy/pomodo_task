from django.db import models
from django.urls import reverse
from django.utils import timezone
from core.abc import CoreModel
from core.constants import PRIORITY_LEVELS
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(CoreModel):
    """
    A task model for Pomodo Task.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="tasks", null=True, blank=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("task-detail", args=[str(self.id)])

    def complete(self):
        self.is_completed = True
        self.updated_at = timezone.now()
        self.save()


class Project(CoreModel):
    """
    A project model for Pomodo Task.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project-detail", args=[str(self.id)])
