from telegram import Bot
from telegram.ext import Updater, CommandHandler
import os
import logging
from celery import shared_task

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    update.message.reply_text('Привет! Я бот, который будет напоминать вам о привычках.')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

@shared_task
def send_reminder(user_id, message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=user_id, text=message)

updater.start_polling()
