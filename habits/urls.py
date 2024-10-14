from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, PublicHabitViewSet

router = DefaultRouter()
router.register(r"", HabitViewSet, basename="habit")
router.register(r"public_habits", PublicHabitViewSet, basename="public_habit")

urlpatterns = [
    path("", include(router.urls)),
]
