# pomodoro/routing.py
from django.urls import re_path
from pomodoro.consumers.pomodoro_consumers import PomodoroSessionConsumer

websocket_urlpatterns = [
    re_path(r"ws/pomodoro-sessions/$", PomodoroSessionConsumer.as_asgi()),
]
