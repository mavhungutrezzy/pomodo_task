from rest_framework import routers
from pomodo_task.tasks.views import ProjectViewSet, TaskViewSet

router = routers.DefaultRouter()

router.register(r"projects", ProjectViewSet, basename="project", )
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = router.urls
