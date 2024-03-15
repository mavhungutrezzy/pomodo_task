from django.utils import timezone
from pomodoro.models import PomodoroSession


class PomodoroService:
    @classmethod
    def start_pomodoro(cls, task, is_break, owner):
        """Start a new Pomodoro session for the given task, break status, and user."""
        return PomodoroSession.objects.create(
            task=task, start_time=timezone.now(), is_break=is_break, owner=owner
        )

    @classmethod
    def pause_pomodoro(cls, pomodoro_session):
        """Pause the given Pomodoro session."""
        pomodoro_session.pause()
        return pomodoro_session

    @classmethod
    def resume_pomodoro(cls, pomodoro_session):
        """Resume the paused Pomodoro session."""
        pomodoro_session.resume()
        return pomodoro_session

    @classmethod
    def stop_pomodoro(cls, pomodoro_session):
        """Stop the given Pomodoro session and update the end time and duration."""
        pomodoro_session.stop()
        return pomodoro_session
