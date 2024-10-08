import os
import logging
from celery import shared_task
from telegram_bot.bot import get_bot_instance  # Импорт функции для получения бота

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Задача для отправки напоминания через Celery
@shared_task
def send_reminder(chat_id, message):
    bot = get_bot_instance()  # Получение экземпляра бота
    try:
        bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Напоминание успешно отправлено в чат {chat_id}")
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение в чат {chat_id}: {e}")
