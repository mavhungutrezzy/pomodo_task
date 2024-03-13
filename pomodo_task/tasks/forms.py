from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Task, Project


class TaskForm(ModelForm):
    """Form for creating and editing tasks."""

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "due_date",
            "priority",
            "is_completed",
            "project",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.none()

    def save(self, commit=True):
        task = super().save(commit=False)
        if self.cleaned_data["project"]:
            task.project = self.cleaned_data["project"]
        if commit:
            task.save()
        return task


class ProjectForm(ModelForm):
    """Form for creating and editing projects."""

    class Meta:
        model = Project
        fields = ["name", "description"]

    def save(self, commit=True):
        project = super().save(commit=False)
        if commit:
            project.save()
        return project
