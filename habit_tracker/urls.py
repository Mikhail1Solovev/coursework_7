from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Настройка Swagger для документации
schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version="v1",
        description="API documentation for the Habit Tracker application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@habittracker.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# URL patterns for main routing
urlpatterns = [
    path("admin/", admin.site.urls),
    # Подключаем маршруты из приложения "habits"
    path("api/habits/", include("habits.urls")),
    # Подключаем маршруты из приложения "users"
    path("api/users/", include("users.urls")),
    # JWT токены для авторизации
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"),
    # Схема API
    path(
        "schema/",
        schema_view.without_ui(
            cache_timeout=0),
        name="api-schema"),
    # Swagger документация
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # ReDoc документация (опционально)
    path(
        "redoc/",
        schema_view.with_ui(
            "redoc",
            cache_timeout=0),
        name="schema-redoc"),
]
