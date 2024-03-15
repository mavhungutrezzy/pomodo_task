from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Pomodoro(models.Model):
    """A model representing a Pomodoro work session."""

    task = models.ForeignKey(
        "tasks.Task", on_delete=models.CASCADE, related_name="pomodoros"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    breaks = models.ManyToManyField(
        "PomodoroBreak", blank=True, related_name="pomodoros"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pomodoros", null=True, blank=True
    )

    class Meta:
        verbose_name = "Pomodoro"
        verbose_name_plural = "Pomodoros"
        app_label = "pomodoro"

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


class PomodoroBreak(models.Model):
    """A model representing a Pomodoro break."""

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_breaks",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Pomodoro Break"
        verbose_name_plural = "Pomodoro Breaks"
        app_label = "pomodoro"

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

    def save(self, *args, **kwargs):
        """Automatically set created_by and updated_by fields."""
        user = getattr(self, "request", None) and self.request.us
