from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'telegram_chat_id']  # Проверьте наличие поля в модели


admin.site.register(CustomUser, CustomUserAdmin)
