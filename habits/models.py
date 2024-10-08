from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Модель пользователя с дополнительными полями
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')

    def __str__(self):
        return self.username

# Модель курса
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_courses')
    is_public = models.BooleanField(default=False, verbose_name='Публичный курс')

    def __str__(self):
        return self.title

# Модель урока, связанного с курсом
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_link = models.URLField(max_length=500, blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(verbose_name='Длительность (минуты)')

    def __str__(self):
        return f"{self.course.title} - {self.title}"

# Модель привычки для курсовой работы
class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    action = models.CharField(max_length=255, verbose_name='Действие')
    place = models.CharField(max_length=255, verbose_name='Место выполнения')
    time = models.TimeField(verbose_name='Время выполнения')
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name='Вознаграждение')
    linked_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Связанная привычка')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    frequency = models.PositiveIntegerField(default=1, verbose_name='Периодичность выполнения (дни)')
    estimated_time = models.PositiveIntegerField(verbose_name='Ожидаемое время выполнения (секунды)')
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError('Приятная привычка не может иметь вознаграждения или связанную привычку.')
        if not self.is_pleasant and not (self.reward or self.linked_habit):
            raise ValidationError('Полезная привычка должна иметь либо вознаграждение, либо связанную привычку.')
        if self.estimated_time > 120:
            raise ValidationError('Ожидаемое время выполнения не должно превышать 120 секунд.')
        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError('Периодичность выполнения должна быть от 1 до 7 дней.')

    def __str__(self):
        return f"{self.user.username} - {self.action}"