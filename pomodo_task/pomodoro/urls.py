from django.urls import path
from . import views

app_name = "pomodoro"


urlpatterns = [
    path("pomodoro/", views.pomodoro_timer, name="pomodoro-timer"),
    path("pomodoro/start/", views.start_pomodoro, name="start-pomodoro"),
    path("pomodoro/stop/", views.stop_pomodoro, name="stop-pomodoro"),
]
