from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("create", views.create_project, name="create_project"),
    path("", views.projects, name="projects"),
    path("create_task", views.create_task, name="create_task"),
]
