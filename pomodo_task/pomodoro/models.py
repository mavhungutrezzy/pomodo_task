from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class PomodoroSession(models.Model):
    """A model representing a Pomodoro session."""

    start_time = models.DateTimeField()
    pause_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(default=timezone.timedelta(minutes=25))
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

    def get_remaining_time(self):
        if self.is_completed or self.is_paused:
            return timedelta(seconds=0)
        elapsed_time = timezone.now() - self.start_time
        remaining_time = self.duration - elapsed_time
        return max(remaining_time, timedelta(seconds=0))

    def check_and_stop_if_elapsed(self):
        if self.get_remaining_time() <= timedelta(seconds=0):
            self.stop()
