from rest_framework import serializers


class ActivitySummarySerializer(serializers.Serializer):
    total_focused_hours = serializers.FloatField()
    days_accessed = serializers.IntegerField()
    day_streak = serializers.IntegerField()


class ActivityDetailsSerializer(serializers.Serializer):
    activity_summary = ActivitySummarySerializer()
    activity_details = serializers.JSONField()
