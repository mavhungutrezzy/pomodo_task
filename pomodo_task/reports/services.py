# services.py
from datetime import timedelta, timezone
from django.db.models import Sum
from pomodoro.models import PomodoroSession


class ActivitySummaryService:
    @classmethod
    def get_total_focused_hours(cls, owner):
        """Get the total focused hours for Pomodoro sessions for the given owner."""
        pomodoro_sessions = PomodoroSession.objects.filter(owner=owner)
        total_duration = pomodoro_sessions.aggregate(total_duration=Sum("duration"))[
            "total_duration"
        ]
        return round(total_duration.total_seconds() / 3600, 2) if total_duration else 0

    @classmethod
    def get_days_accessed(cls, owner):
        """Get the number of days accessed for the given owner."""
        pomodoro_sessions = PomodoroSession.objects.filter(owner=owner)
        return (
            pomodoro_sessions.dates("start_time", "day", order="DESC")
            .distinct()
            .count()
        )

    @classmethod
    def get_day_streak(cls, owner):
        """Get the longest day streak for the given owner."""
        pomodoro_sessions = PomodoroSession.objects.filter(owner=owner)
        return (
            pomodoro_sessions.dates("start_time", "day", order="DESC")
            .distinct()
            .count()
        )

    @classmethod
    def get_activity_summary(cls, owner):
        """Get the activity summary for the given owner."""
        return {
            "total_focused_hours": cls.get_total_focused_hours(owner),
            "days_accessed": cls.get_days_accessed(owner),
            "day_streak": cls.get_day_streak(owner),
        }

    @classmethod
    def get_activity_details(
        cls, owner, start_date=None, end_date=None, time_range=None
    ):
        pomodoro_sessions = PomodoroSession.objects.filter(owner=owner)

        if start_date and end_date:
            pomodoro_sessions = pomodoro_sessions.filter(
                start_time__date__range=[start_date, end_date]
            )

        if time_range:
            if time_range == "week":
                pomodoro_sessions = pomodoro_sessions.filter(
                    start_time__date__range=[
                        start_date or (end_date - timedelta(days=7)),
                        end_date or timezone.now().date(),
                    ]
                )
            elif time_range == "month":
                pomodoro_sessions = pomodoro_sessions.filter(
                    start_time__year=(start_date or end_date).year,
                    start_time__month=(start_date or end_date).month,
                )
            elif time_range == "year":
                pomodoro_sessions = pomodoro_sessions.filter(
                    start_time__year=(start_date or end_date).year,
                )

        return pomodoro_sessions.values(
            "task__name",
            "task__project__name",
            "start_time__date",
            "duration",
        )
