from celery import shared_task
import asyncio
from telegram_bot.bot import get_bot_instance

@shared_task
def send_reminder(chat_id, message):
    bot = get_bot_instance()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.send_message(chat_id=chat_id, text=message))
