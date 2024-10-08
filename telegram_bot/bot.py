import os
import logging
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from celery import shared_task

# Load Telegram Bot Token from environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    raise ValueError("Telegram token not found. Please set TELEGRAM_TOKEN in environment variables.")

bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a sample command to test the bot
def start(update, context):
    update.message.reply_text('Welcome! This is your Habit Reminder Bot.')

# Command handler for /start
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Sample Celery task to send reminders
@shared_task
def send_reminder(chat_id, message):
    bot.send_message(chat_id=chat_id, text=message)

# Start the bot (this should be run in a separate process)
if __name__ == '__main__':
    updater.start_polling()
    updater.idle()