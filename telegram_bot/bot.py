from telegram import Bot
from telegram.ext import Updater, CommandHandler
import os
import logging
from celery import shared_task

# Telegram bot settings
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Настройка бота
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Логирование для мониторинга работы бота
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Команда /start, которую можно вызвать пользователем в Телеграме
def start(update, context):
    update.message.reply_text('Привет! Я бот, который будет напоминать вам о привычках.')

# Добавление обработчика для команды /start
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

@shared_task
def send_reminder(user_id, message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=user_id, text=message)

# Запуск бота
updater.start_polling()
