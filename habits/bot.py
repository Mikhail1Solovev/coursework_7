import telebot
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Initialize bot with token from environment variables
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Привет, чем я могу тебе помочь?")
    elif message.text.lower() == "/help":
        bot.send_message(message.chat.id, "Напиши привет")
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help.")

@bot.message_handler(content_types=['document', 'audio'])
def handle_other_types(message):
    pass