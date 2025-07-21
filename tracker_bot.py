import os
import json
import logging
from datetime import datetime, timedelta
from telegram import Bot

# Import scrapers (you’ll add these files next)
from sources.predictz import get_predictz_tips
from sources.forebet import get_forebet_tips
from sources.windrawwin import get_windrawwin_tips
from utils.dedupe import load_sent_matches, save_sent_matches

# === Setup ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DAYS_TO_SCAN = 3

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)

def merge_tips(*tipster_lists):
    combined = {}
    for tips in tipster_lists:
        for tip in tips:
            key = f"{tip['date']}|{tip['match']}|{tip['market']}"
            if key not in combined:
                combined[key] = {
                    'date': tip['date'],
                    'match': tip['match'],
                    'market': tip['market'],
                    'prediction': tip['prediction'],
                    'sources': [tip['source']],
                    'confidences': [tip['confidence']],
                }
            else:
                combined[key]['sources'].append(tip['source'])
                combined[key]['confidences'].append(tip['confidence'])
    return combined

def format_message(tips_dict):
    message = "📊 Tipster Consensus – Next 3 Days 🔥\n\n"
    for tip in tips_dict.values():
        if len(tip['sources']) >= 2:
            confidence_avg = sum(tip['confidences']) / len(tip['confidences'])
            message += (
                f"🏟️ {tip['match']} ({tip['date']})\n"
                f"💡 Market: {tip['market']} – {tip['prediction']}\n"
                f"📈 Avg Confidence: {round(confidence_avg)}%\n"
                f"📚 Tipsters: {', '.join(tip['sources'])}\n\n"
            )
    return message.strip()

def main():
    today = datetime.today()
    date_range = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(DAYS_TO_SCAN)]
    
    logging.info("📥 Collecting tips from tipsters...")
    tips_predictz = get_predictz_tips(date_range)
    tips_forebet = get_forebet_tips(date_range)
    tips_wdw = get_windrawwin_tips(date_range)

    tips = merge_tips(tips_predictz, tips_forebet, tips_wdw)
    sent = load_sent_matches()

    new_tips = {}
    for key, tip in tips.items():
        if key not in sent and len(tip['sources']) >= 2:
            new_tips[key] = tip

    if not new_tips:
        logging.info("No new high-confidence tips today.")
        return

    message = format_message(new_tips)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    logging.info("✅ Sent tips to Telegram.")

    save_sent_matches(list(new_tips.keys()))

if __name__ == "__main__":
    main()
