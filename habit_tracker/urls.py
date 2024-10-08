from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/habits/', include('habits.urls')),  # Подключаем маршруты из приложения "habits"
    path('api/users/', include('users.urls')),  # Подключаем маршруты из приложения "users"
]
