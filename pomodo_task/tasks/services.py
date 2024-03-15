from tasks.models import Task, Project
from django.shortcuts import get_object_or_404


class BaseService:
    """Base class for all services."""

    model = None

    @classmethod
    def create(cls, **kwargs):
        obj = cls.model(**kwargs)
        obj.save()
        return obj

    @classmethod
    def update(cls, obj, **kwargs):
        for field, value in kwargs.items():
            setattr(obj, field, value)
        obj.save()
        return obj

    @staticmethod
    def delete(obj):
        obj.delete()  # soft delete

    @classmethod
    def get_by_id(cls, obj_id):
        return get_object_or_404(cls.model, pk=obj_id)


class TaskService(BaseService):
    """Service class for tasks."""

    model = Task

    @classmethod
    def create_task(cls, owner, name, description, due_date, priority, project):
        return cls.create(
            owner=owner,
            name=name,
            description=description,
            due_date=due_date,
            priority=priority,
            project=project,
        )

    @classmethod
    def get_all_tasks(cls, owner):
        return cls.model.objects.filter(owner=owner)

    @classmethod
    def update_task(cls, task, name, description, due_date, priority, project):
        return cls.update(
            task,
            name=name,
            description=description,
            due_date=due_date,
            priority=priority,
            project=project,
        )

    @classmethod
    def get_task_by_id(cls, task_id):
        return cls.model.objects.get(id=task_id)

    @classmethod
    def complete_task(cls, task):
        return cls.update(task, is_completed=True)

    @classmethod
    def delete_task(cls, task):
        return cls.delete(task)


class ProjectService(BaseService):
    """Service class for projects."""

    model = Project

    @classmethod
    def create_project(cls, owner, name, description):
        return cls.create(owner=owner, name=name, description=description)

    @classmethod
    def update_project(cls, project, name, description):
        return cls.update(project, name=name, description=description)

    @classmethod
    def get_all_projects(cls, owner):
        return cls.model.objects.filter(owner=owner)

    @classmethod
    def get_project_by_id(cls, project_id):
        return cls.model.objects.get(id=project_id)

    @classmethod
    def delete_project(cls, project):
        return cls.delete(project)

    @classmethod
    def get_all_tasks_in_project(cls, project):
        return cls.model.objects.get(id=project.id).tasks
