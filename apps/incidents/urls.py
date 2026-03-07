from rest_framework.routers import DefaultRouter
from .views import IncidentViewSet, CorrectiveActionViewSet, NotificationViewSet

router = DefaultRouter()
router.register("incidents", IncidentViewSet, basename="incident")
router.register("actions", CorrectiveActionViewSet, basename="correctiveaction")
router.register('notifications', NotificationViewSet, basename='notifications')
urlpatterns = router.urls