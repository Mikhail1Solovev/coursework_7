from django.contrib import admin
from .models import UserHabit

@admin.register(UserHabit)
class UserHabitAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'action',
        'execution_time',
        'is_pleasant',
        'periodicity']
    search_fields = ['user__email', 'action']
    list_filter = ['is_pleasant', 'periodicity']
