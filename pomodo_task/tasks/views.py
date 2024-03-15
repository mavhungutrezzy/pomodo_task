from django.shortcuts import redirect, render
from .services import ProjectService, TaskService
from .forms import ProjectForm, TaskForm


def create_project(request):
    projects = ProjectService.get_all_projects()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = ProjectService.create_project(
                request.user,
                form.cleaned_data["name"],
                form.cleaned_data["description"],
            )
            return render(request, "tasks/create_project.html", {"project": project})
    else:
        form = ProjectForm()

    return render(
        request, "tasks/create_project.html", {"form": form, "projects": projects}
    )


def projects(request):
    projects = ProjectService.get_all_projects()
    return render(request, "tasks/projects.html", {"projects": projects})


def create_task(request):
    if request.method == "POST":
        project = ProjectService.get_project_by_id(request.POST.get("project"))
        data = {
            "name": request.POST.get("name"),
            "description": request.POST.get("description"),
            "due_date": request.POST.get("due_date"),
            "priority": request.POST.get("priority"),
            "project": project,
            "user": request.user,
        }

        TaskService.create_task(**data)

        return redirect("tasks:projects")
    else:
        form = TaskForm()

    projects = ProjectService.get_all_projects()
    return render(
        request, "tasks/create_task.html", {"form": form, "projects": projects}
    )
