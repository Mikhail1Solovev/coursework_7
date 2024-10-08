from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, HabitViewSet

# Создаем роутер для автоматической маршрутизации
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'habits', HabitViewSet, basename='habit')

# Подключаем маршруты роутера
urlpatterns = [
    path('', include(router.urls)),
]