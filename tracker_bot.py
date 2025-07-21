import logging
import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Logging ===
logging.basicConfig(
    format="%(asctime)s — %(levelname)s — %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# === Your credentials ===
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
GOOGLE_SHEET_NAME = "YOUR_SHEET_NAME"
GOOGLE_CREDS_FILE = "credentials.json"  # must be uploaded to your project

# === Google Sheet Setup ===
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# === Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Tracker Bot is active!")

async def show_matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        if df.empty:
            await update.message.reply_text("No match data available.")
            return

        message = "📋 Tipster Matches:\n\n"
        for i, row in df.iterrows():
            message += f"{row.get('Match', 'N/A')} | {row.get('Market', 'N/A')} | {row.get('Tip', 'N/A')}\n"

        await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        await update.message.reply_text("⚠️ Failed to fetch match data.")

# === Main Setup ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("show", show_matches))

    logger.info("🤖 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
