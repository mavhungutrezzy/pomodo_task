from rest_framework import serializers
from tasks.models import Project, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("owner",)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("owner",)
