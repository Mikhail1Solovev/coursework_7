from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import UserHabit  # Исправлено
from .serializers import UserHabitSerializer  # Исправлено
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class HabitPagination(PageNumberPagination):
    page_size = 5


class HabitViewSet(viewsets.ModelViewSet):
    queryset = UserHabit.objects.all()  # Исправлено
    serializer_class = UserHabitSerializer  # Исправлено
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        # Отправка напоминания через Celery (если требуется)
        send_reminder.apply_async(args=[self.request.user.chat_id, f"Напоминание о привычке: {habit.action}"], countdown=habit.reminder_time)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserHabit.objects.filter(is_public=True)  # Исправлено
    serializer_class = UserHabitSerializer  # Исправлено
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = HabitPagination
