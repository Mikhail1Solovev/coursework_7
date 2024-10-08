from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    frequency = models.PositiveIntegerField(default=1)  # Frequency in days, default daily
    reward = models.CharField(max_length=255, null=True, blank=True)
    estimated_time = models.PositiveIntegerField()  # Estimated time in seconds
    is_public = models.BooleanField(default=False)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError('Pleasant habits cannot have rewards or linked habits.')
        if not self.is_pleasant and not (self.reward or self.linked_habit):
            raise ValidationError('Either reward or linked habit must be specified for a useful habit.')
        if self.estimated_time > 120:
            raise ValidationError('Estimated time must not exceed 120 seconds.')
        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError('Frequency must be between 1 and 7 days.')
