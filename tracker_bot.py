import os
import logging
import requests
import datetime
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot credentials (set via environment variables on Render)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Command handler for /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Tipster Tracker Bot is online and working!")

# Sample command to show today's date
def today(update: Update, context: CallbackContext):
    today_date = datetime.datetime.now().strftime("%A, %d %B %Y")
    update.message.reply_text(f"📅 Today is {today_date}")

# Main function to launch bot
if __name__ == '__main__':
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("today", today))

    # Start polling
    logger.info("[+] Bot started. Listening for commands...")
    updater.start_polling()
    updater.idle()
