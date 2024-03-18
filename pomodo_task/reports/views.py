# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from reports.serializers import ActivityDetailsSerializer
from reports.services import ActivitySummaryService


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
