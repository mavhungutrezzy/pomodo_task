from django.db import models
from django.urls import reverse
from django.utils import timezone
from core.abc import CoreModel


class Pomodoro(CoreModel):
    """
    A model representing a Pomodoro work session.
    """

    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="pomodoros")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    breaks = models.ManyToManyField(
        "PomodoroBreak", blank=True, related_name="pomodoros"
    )

    def __str__(self):
        return f"Pomodoro for {self.task.name}"

    def start(self):
        """Start the Pomodoro session."""
        self.start_time = timezone.now()
        self.save()

    def stop(self):
        """Stop the Pomodoro session and calculate the duration."""
        self.end_time = timezone.now()
        self.duration = self.end_time - self.start_time
        self.is_completed = True
        self.save()

    def get_absolute_url(self):
        return reverse("pomodoro-detail", args=[str(self.id)])


class PomodoroBreak(CoreModel):
    """
    A model representing a Pomodoro break.
    """

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Pomodoro Break started at {self.start_time}"

    def start(self):
        """Start the Pomodoro break."""
        self.start_time = timezone.now()
        self.save()

    def stop(self):
        """Stop the Pomodoro break and calculate the duration."""
        self.end_time = timezone.now()
        self.duration = self.end_time - self.start_time
        self.is_completed = True
        self.save()

    def get_absolute_url(self):
        return reverse("pomodoro-break-detail", args=[str(self.id)])
