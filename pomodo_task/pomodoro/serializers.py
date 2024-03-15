from rest_framework import serializers
from pomodoro.models import PomodoroSession


class PomodoroSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PomodoroSession
        fields = [
            "id",
            "start_time",
            "pause_time",
            "end_time",
            "duration",
            "is_completed",
            "is_paused",
            "is_break",
            "task",
        ]
        read_only_fields = [
            "start_time",
            "pause_time",
            "end_time",
            "duration",
            "is_completed",
            "is_paused",
            "owner",
        ]


class PomodoroSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PomodoroSession
        fields = ["task", "is_break"]
