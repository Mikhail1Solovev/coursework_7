import os
import logging
from celery import shared_task
from dotenv import load_dotenv
from telegram_bot.bot import get_bot_instance

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample Celery task to send reminders
@shared_task
def send_reminder(chat_id, message):
    bot = get_bot_instance()
    try:
        bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Message successfully sent to chat_id {chat_id}")
    except Exception as e:
        logger.error(f"Failed to send message to chat_id {chat_id}: {e}")
