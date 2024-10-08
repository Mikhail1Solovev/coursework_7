import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Telegram Bot Token from environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    raise ValueError(
        "Telegram token not found. Please set TELEGRAM_TOKEN in environment "
        "variables."
    )

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to get Bot instance


def get_bot_instance():
    return Bot(token=TELEGRAM_TOKEN)

# Define a sample command to test the bot


def start(update, context):
    update.message.reply_text('Welcome! This is your Habit Reminder Bot.')


# Create Application using the token and add command handlers
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

# Start the bot (this should be run in a separate process)
if __name__ == '__main__':
    application.run_polling()
