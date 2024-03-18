import csv
from django.http import HttpResponse
from pomodoro.serializers import PomodoroSessionSerializer
from tasks.serializers import ProjectSerializer, TaskSerializer

CSV_HEADERS = {
    "Tasks": TaskSerializer.Meta.fields,
    "Projects": ProjectSerializer.Meta.fields,
    "Pomodoro Sessions": PomodoroSessionSerializer.Meta.fields,
}


def create_csv_response():
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="activity_details.csv"'
    return response


def write_csv_data(response, section_name, data, CSV_HEADERS):
    writer = csv.writer(response)
    writer.writerow([section_name])
    writer.writerow(CSV_HEADERS[section_name])
    serializer = get_serializer(section_name, data)
    for item in serializer.data:
        writer.writerow(item.values())


def get_serializer(section_name, data):
    if section_name == "Tasks":
        serializer_class = TaskSerializer
    elif section_name == "Projects":
        serializer_class = ProjectSerializer
    elif section_name == "Pomodoro Sessions":
        serializer_class = PomodoroSessionSerializer
    return serializer_class(data, many=True)
