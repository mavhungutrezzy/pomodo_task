from pomodoro.serializers import PomodoroSessionSerializer
from rest_framework import serializers
from tasks.serializers import ProjectSerializer, TaskSerializer


class ActivitySummarySerializer(serializers.Serializer):
    total_focused_hours = serializers.FloatField()
    days_accessed = serializers.IntegerField()
    day_streak = serializers.IntegerField()


class ActivityDetailsSerializer(serializers.Serializer):
    activity_summary = ActivitySummarySerializer()
    activity_details = serializers.JSONField()


class ExportReportSerializer(serializers.Serializer):
    pomodoro_sessions = PomodoroSessionSerializer(many=True)
    tasks = TaskSerializer(many=True)
    projects = ProjectSerializer(many=True)
