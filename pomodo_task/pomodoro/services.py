from django.utils import timezone
from pomodoro.models import Pomodoro, PomodoroBreak


class PomodoroService:
    @classmethod
    def start_pomodoro(cls, task, user):
        """Start a new Pomodoro session for the given task and user."""
        return Pomodoro.objects.create(
            task=task, start_time=timezone.now(), created_by=user
        )

    @classmethod
    def stop_pomodoro(cls, pomodoro):
        """Stop the given Pomodoro session and update the end time and duration."""
        pomodoro.end_time = timezone.now()
        pomodoro.duration = pomodoro.end_time - pomodoro.start_time
        pomodoro.is_completed = True
        pomodoro.save()
        return pomodoro

    @classmethod
    def start_break(cls, duration=25):
        """Start a new Pomodoro break with the given duration (in minutes)."""
        break_duration = timezone.timedelta(minutes=duration)
        return PomodoroBreak.objects.create(
            start_time=timezone.now(), duration=break_duration
        )

    @classmethod
    def stop_break(cls, pomodoro_break):
        """Stop the given Pomodoro break and update the end time and duration."""
        pomodoro_break.end_time = timezone.now()
        pomodoro_break.duration = pomodoro_break.end_time - pomodoro_break.start_time
        pomodoro_break.is_completed = True
        pomodoro_break.save()
        return pomodoro_break

    @classmethod
    def add_break_to_pomodoro(cls, pomodoro, pomodoro_break):
        """Associate the given Pomodoro break with the given Pomodoro session."""
        pomodoro.breaks.add(pomodoro_break)

    @classmethod
    def get_pomodoro_by_id(cls, pomodoro_id):
        """Retrieve a Pomodoro instance by its ID."""
        return Pomodoro.objects.get(id=pomodoro_id)

    @classmethod
    def get_break_by_id(cls, break_id):
        """Retrieve a PomodoroBreak instance by its ID."""
        return PomodoroBreak.objects.get(id=break_id)

    @classmethod
    def get_completed_pomodoros(cls, user):
        return Pomodoro.objects.filter(end_time__isnull=False, created_by=user)


    @classmethod
    def get_ongoing_pomodoro(cls):
        return Pomodoro.objects.filter(end_time__isnull=True)
