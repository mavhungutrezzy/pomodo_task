from rest_framework import routers
from pomodo_task.tasks.views import ProjectViewSet, TaskViewSet
from pomodo_task.pomodoro.views import PomodoroSessionViewSet
from pomodo_task.reports.views import ActivitySummaryViewSet

router = routers.DefaultRouter()

router.register(
    r"projects",
    ProjectViewSet,
    basename="project",
)
router.register(r"tasks", TaskViewSet, basename="task")
router.register(
    r"pomodoro-sessions", PomodoroSessionViewSet, basename="pomodoro-session"
)
router.register(
    r"reports/activity-summary", ActivitySummaryViewSet, basename="activity-summary"
)


urlpatterns = router.urls
