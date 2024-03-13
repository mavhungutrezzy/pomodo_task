from tasks.models import Task, Project
from django.shortcuts import get_object_or_404


class BaseService:
    """Base class for all services."""

    model = None

    @classmethod
    def create(cls, user, **kwargs):
        obj = cls.model(**kwargs, created_by=user)
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

    @staticmethod
    def get_by_id(obj_id):
        return get_object_or_404(BaseService.model, pk=obj_id)


class TaskService(BaseService):
    """Service class for tasks."""

    model = Task

    @classmethod
    def create_task(cls, user, name, description, due_date, priority, project):
        return cls.create(
            user,
            name=name,
            description=description,
            due_date=due_date,
            priority=priority,
            project=project,
        )

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


class ProjectService(BaseService):
    """Service class for projects."""

    model = Project

    @classmethod
    def create_project(cls, user, name, description):
        return cls.create(user, name=name, description=description)

    @classmethod
    def update_project(cls, project, name, description):
        return cls.update(project, name=name, description=description)
