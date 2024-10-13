from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import UserHabit  # Исправлено
from .serializers import UserHabitSerializer  # Исправлено
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from telegram_bot.tasks import send_reminder


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

        # Проверка наличия времени напоминания перед отправкой задачи
        if hasattr(habit, 'reminder_time') and habit.reminder_time:
            send_reminder.apply_async(
                args=[self.request.user.telegram_chat_id, f"Напоминание о привычке: {habit.action}"],
                countdown=habit.reminder_time * 60  # Задержка в секундах (пример в минутах)
            )


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserHabit.objects.filter(is_public=True)  # Исправлено
    serializer_class = UserHabitSerializer  # Исправлено
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = HabitPagination
