from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from django.urls import path, include
from django.contrib import admin

title = "Habit Tracker API"
description = "API documentation for the Habit Tracker application."
schema_view = get_schema_view(title=title, description=description)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/habits/', include('habits.urls')),  # Подключаем маршруты из приложения "habits"
    path('api/users/', include('users.urls')),  # Подключаем маршруты из приложения "users"
    path('schema/', schema_view, name='api-schema'),
    path('docs/', include_docs_urls(title=title, description=description)),
]
