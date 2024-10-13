import os
from celery import Celery
from django.conf import settings
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')

app = Celery('habit_tracker')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

CELERY_BEAT_SCHEDULE = {
    'send_reminder': {
        'task': 'telegram_bot.tasks.send_reminder',
        'schedule': timedelta(hours=1),  # Настроить по необходимости
        'args': ['<CHAT_ID>', 'Напоминание о привычке']
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
