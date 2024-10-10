from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from habits.models import positive_integer_validator


class CustomUser(AbstractUser):
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


class UserHabit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
