from django.db import models
from django.urls import reverse
from django.utils import timezone
from core.constants import PRIORITY_LEVELS
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_tasks",
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True
    )

    def __str__(self):
        return self.name

    def complete(self):
        self.is_completed = True
        self.updated_at = timezone.now()
        self.save()
