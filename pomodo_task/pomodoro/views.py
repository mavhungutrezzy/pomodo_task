from django.utils.timezone import timedelta
from pomodoro.models import PomodoroSession
from pomodoro.serializers import (PomodoroSessionCreateSerializer,
                                  PomodoroSessionSerializer)
from pomodoro.services import PomodoroService
from rest_framework import status, viewsets
from rest_framework.response import Response


class PomodoroSessionViewSet(viewsets.ModelViewSet):
    queryset = PomodoroSession.objects.all()
    serializer_class = PomodoroSessionSerializer

    def create(self, request, *args, **kwargs):
        serializer = PomodoroSessionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pomodoro_session = PomodoroService.start_pomodoro(
            task=serializer.validated_data["task"],
            is_break=serializer.validated_data["is_break"],
            owner=request.user,
            duration=serializer.validated_data.get("duration"),
        )
        response_serializer = self.get_serializer(pomodoro_session)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if "action" not in request.data:
            return Response(
                {"error": "Action is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        action = request.data["action"]
        if action == "pause":
            pomodoro_session = PomodoroService.pause_pomodoro(instance)
        elif action == "resume":
            pomodoro_session = PomodoroService.resume_pomodoro(instance)
        elif action == "stop":
            pomodoro_session = PomodoroService.stop_pomodoro(instance)
        else:
            return Response(
                {"error": "Invalid action provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        response_serializer = self.get_serializer(pomodoro_session)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
