from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def positive_integer_validator(value):
    if value <= 0:
        raise ValidationError(
            f'Value must be positive, got {value}.'
        )


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='related_habits'
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        validators=[positive_integer_validator]
    )  # Периодичность выполнения в днях
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    execution_time = models.PositiveIntegerField(
        validators=[positive_integer_validator]
    )  # Время на выполнение в секундах
    is_public = models.BooleanField(default=False)

    def clean(self):
        # Валидация: нельзя выбирать одновременно вознаграждение и
        # связанную привычку
        if self.reward and self.linked_habit:
            raise ValidationError(
                'Можно заполнить либо вознаграждение, либо связанную '
                'привычку, но не оба поля одновременно.'
            )
        # Время выполнения должно быть не более 120 секунд
        if self.execution_time > 120:
            raise ValidationError(
                'Время выполнения привычки не может превышать 120 секунд.'
            )
        # Периодичность должна быть не реже одного раза в неделю
        if self.periodicity > 7:
            raise ValidationError(
                'Периодичность выполнения привычки должна быть не реже '
                'одного раза в неделю.'
            )

    def __str__(self):
        return f"{self.action} ({self.user.username})"
