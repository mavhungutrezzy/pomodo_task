from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from pomodoro.models import PomodoroSession


class PomodoroService:
    @classmethod
    def start_pomodoro(cls, task, is_break, owner, duration):
        """Start a new Pomodoro session for the given task, break status, user, and duration."""
        return PomodoroSession.objects.create(
            task=task,
            start_time=timezone.now(),
            is_break=is_break,
            owner=owner,
            duration=duration,
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
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "pomodoro_sessions",
            {
                "type": "session_completed",
                "session_id": pomodoro_session.id,
            },
        )
        return pomodoro_session
