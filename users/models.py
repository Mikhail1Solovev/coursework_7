from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from habits.models import positive_integer_validator  # Если это используется


class UserHabit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    periodicity = models.PositiveIntegerField(
        validators=[positive_integer_validator]
    )
    execution_time = models.PositiveIntegerField()

    def clean(self):
        if self.execution_time > 120:
            raise ValidationError(
                'Время выполнения привычки не может превышать 120 секунд.'
            )

    def __str__(self):
        return f"{self.action} ({self.user.username})"
