from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'time', 'is_public', 'is_pleasant', 'periodicity']
    search_fields = ['user__username', 'action']
    list_filter = ['is_public', 'is_pleasant', 'periodicity']
