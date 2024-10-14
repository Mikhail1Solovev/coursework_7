import logging
from celery import shared_task

# Импорт функции для получения бота
from telegram_bot.bot import get_bot_instance

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@shared_task
def send_reminder(chat_id, message):
    bot = get_bot_instance()
    try:
        bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Напоминание успешно отправлено в чат {chat_id}")
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение в чат {chat_id}: {e}")
