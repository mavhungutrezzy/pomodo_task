from django.contrib import admin
from .models import Pomodoro, PomodoroBreak


@admin.register(Pomodoro)
class PomodoroAdmin(admin.ModelAdmin):
    list_display = ("task", "start_time", "end_time", "duration", "is_completed")


@admin.register(PomodoroBreak)
class PomodoroBreakAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time", "duration", "is_completed")
