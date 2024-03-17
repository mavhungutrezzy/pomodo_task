from core.permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from tasks.serializers import ProjectSerializer, TaskSerializer
from tasks.services import ProjectService, TaskService

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return ProjectService.get_all_projects(owner=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ProjectService.create_project(
            owner=request.user,
            name=serializer.validated_data["name"],
            description=serializer.validated_data["description"],
        )
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        ProjectService.update_project(
            instance,
            serializer.validated_data["name"],
            serializer.validated_data["description"],
        )
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ProjectService.delete_project(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk):
        project = self.get_object()
        tasks = ProjectService.get_all_tasks_in_project(project)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        owner = self.request.user
        return TaskService.get_all_tasks(owner)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        TaskService.create_task(
            owner=request.user,
            name=serializer.validated_data["name"],
            description=serializer.validated_data["description"],
            due_date=serializer.validated_data["due_date"],
            priority=serializer.validated_data["priority"],
            project=serializer.validated_data["project"],
        )
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        TaskService.update_task(
            instance,
            serializer.validated_data["name"],
            serializer.validated_data["description"],
            serializer.validated_data["due_date"],
            serializer.validated_data["priority"],
            serializer.validated_data["project"],
        )
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        TaskService.delete_task(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
