from django.contrib import admin
from pomodoro.models import PomodoroSession


@admin.register(PomodoroSession)
class PomodoroSessionAdmin(admin.ModelAdmin):
    list_display = ("task", "start_time", "end_time", "duration")
