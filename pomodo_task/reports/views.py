from django.http import HttpResponse
from reports.serializers import ActivityDetailsSerializer
from reports.services import ActivitySummaryService
from rest_framework import viewsets
from rest_framework.response import Response


from .export_helpers import (
    write_csv_data,
    create_csv_response,
    CSV_HEADERS,
)


class ActivitySummaryViewSet(viewsets.ViewSet):

    def list(self, request):
        user = request.user
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        activity_summary = ActivitySummaryService.get_activity_summary(user)
        activity_details = ActivitySummaryService.get_activity_details(
            user, start_date, end_date
        )

        data = {
            "activity_summary": activity_summary,
            "activity_details": activity_details,
        }
        serializer = ActivityDetailsSerializer(data)
        return Response(serializer.data)


class ExportActivityDetailsView(viewsets.ViewSet):

    def get(self, request):
        response = create_csv_response()

        owner = request.user
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        time_range = request.query_params.get("time_range")

        tasks, projects, pomodoro_sessions = (
            ActivitySummaryService.export_activity_details(
                owner, start_date, end_date, time_range
            )
        )

        for name, data in zip(
            ["Tasks", "Projects", "Pomodoro Sessions"],
            [tasks, projects, pomodoro_sessions],
        ):
            write_csv_data(response, name, data, CSV_HEADERS)

        return response
