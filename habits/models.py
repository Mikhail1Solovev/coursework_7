from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError


class UserHabit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    periodicity = models.PositiveIntegerField(
        help_text='Периодичность выполнения привычки в днях.'
    )
    execution_time = models.PositiveIntegerField(
        help_text='Время выполнения привычки в секундах.'
    )
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='linked_habits', help_text='Связанная привычка')
    reward = models.CharField(max_length=255, blank=True, null=True, help_text='Вознаграждение за выполнение привычки')
    is_pleasant = models.BooleanField(default=False, help_text='Является ли привычка приятной')
    is_public = models.BooleanField(default=False, help_text='Является ли привычка публичной')  # Добавлено поле

    def clean(self):
        # Проверка времени выполнения
        if self.execution_time > 120:
            raise ValidationError('Время выполнения привычки не может превышать 120 секунд.')

        # Периодичность должна быть не реже одного раза в 7 дней
        if self.periodicity > 7:
            raise ValidationError('Периодичность привычки должна быть не реже одного раза в 7 дней.')

        # Нельзя одновременно выбрать связанную привычку и указать вознаграждение
        if self.reward and self.linked_habit:
            raise ValidationError('Нельзя одновременно указать связанную привычку и вознаграждение.')

        # Связанной привычкой может быть только приятная привычка
        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError('Связанной привычкой может быть только приятная привычка.')

        # Приятной привычке нельзя назначить связанную привычку или вознаграждение
        if self.is_pleasant and (self.linked_habit or self.reward):
            raise ValidationError('Приятной привычке нельзя назначить связанную привычку или вознаграждение.')

    def __str__(self):
        return f"{self.action} ({self.user.email})"
