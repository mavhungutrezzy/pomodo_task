from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class PomodoroSession(models.Model):
    """A model representing a Pomodoro session."""

    start_time = models.DateTimeField()
    pause_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    is_break = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    task = models.ForeignKey(
        "tasks.Task", on_delete=models.CASCADE, related_name="pomodoro_sessions"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pomodoro_sessions",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Pomodoro Session"
        verbose_name_plural = "Pomodoro Sessions"
        app_label = "pomodoro"

    def __str__(self):
        return f"Pomodoro Session for {self.task.name}"

    def start(self):
        """Start the Pomodoro session."""
        self.start_time = timezone.now()
        self.save()

    def pause(self):
        """Pause the Pomodoro session."""
        self.pause_time = timezone.now()
        self.is_paused = True
        self.save()

    def resume(self):
        """Resume the paused Pomodoro session."""
        if self.is_paused:
            self.start_time += timezone.now() - self.pause_time
            self.pause_time = None
            self.is_paused = False
            self.save()

    def stop(self):
        """Stop the Pomodoro session and calculate the duration."""
        self.end_time = timezone.now()
        self.duration = self.end_time - self.start_time
        self.is_completed = True
        self.save()
