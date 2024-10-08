from celery import shared_task
from .models import Habit
from django.utils import timezone
from telegram_bot.bot import bot  # Import the bot from bot.py

@shared_task
def send_habit_reminders():
    # Получаем текущее время
    current_time = timezone.now().time()
    # Фильтруем привычки, которые должны выполняться в текущее время
    habits = Habit.objects.filter(time__hour=current_time.hour, time__minute=current_time.minute)

    for habit in habits:
        if hasattr(habit.user, 'telegram_chat_id') and habit.user.telegram_chat_id:
            bot.send_message(habit.user.telegram_chat_id, f"Reminder: {habit.action} at {habit.place}")
