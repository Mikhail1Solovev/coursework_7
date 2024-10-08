from django.urls import path, include
from django.contrib import admin
from .api_docs import schema_view, include_docs_urls

# URL patterns for main routing
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/habits/', include('habits.urls')),  # Подключаем маршруты из приложения "habits"
    path('api/users/', include('users.urls')),  # Подключаем маршруты из приложения "users"
    path('schema/', schema_view, name='api-schema'),
    path('docs/', include_docs_urls(title="Habit Tracker API", description="API documentation for the Habit Tracker application.")),
]