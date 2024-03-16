from rest_framework import serializers
from pomodoro.models import PomodoroSession


class PomodoroSessionSerializer(serializers.ModelSerializer):
    remaining_time = serializers.SerializerMethodField()

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
            "remaining_time",
        ]
        read_only_fields = [
            "start_time",
            "pause_time",
            "end_time",
            "duration",
            "is_completed",
            "is_paused",
            "remaining_time",
            "owner",
        ]

    def get_remaining_time(self, obj):
        return obj.get_remaining_time()


class PomodoroSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PomodoroSession
        fields = ["task", "is_break", "duration"]
