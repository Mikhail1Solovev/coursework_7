from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from habits.models import positive_integer_validator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле email должно быть заполнено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False)

    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='Группы, к которым принадлежит пользователь.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Конкретные права для данного пользователя.',
        verbose_name='user permissions'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Оставляем пустым, так как username не используется

    def __str__(self):
        return self.email


class UserHabit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    periodicity = models.PositiveIntegerField(
        validators=[positive_integer_validator],
        help_text='Периодичность выполнения привычки в днях.'
    )
    execution_time = models.PositiveIntegerField(
        help_text='Время выполнения привычки в секундах.'
    )
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='linked_habits', help_text='Связанная привычка')
    reward = models.CharField(max_length=255, blank=True, null=True, help_text='Вознаграждение за выполнение привычки')
    is_pleasant = models.BooleanField(default=False, help_text='Является ли привычка приятной')

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
