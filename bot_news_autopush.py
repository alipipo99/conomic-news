import os
import requests
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from telegram import Bot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

sources = [
    ("https://www.bloomberg.com", "Bloomberg"),
    ("https://www.cnbc.com/economy/", "CNBC"),
    ("https://tradingeconomics.com", "TradingEconomics"),
    ("https://cointelegraph.com", "Cointelegraph"),
    ("https://www.theblock.co", "The Block"),
    ("https://www.lookonchain.com", "Lookonchain"),
]

headlines = []

for url, source in sources:
    try:
        resp = requests.get(url, timeout=10)
        lines = resp.text.split("\n")
        for line in lines:
            if "<title>" in line.lower():
                title = line.strip().replace("<title>", "").replace("</title>", "")
                title = title.split("|")[0].strip()
                translated = GoogleTranslator(source='auto', target='fa').translate(title)
                headlines.append(f"📰 {translated} ({source})")
                break
    except Exception as e:
        headlines.append(f"⚠️ خطا در دریافت از {source}")

message = "📡 *آخرین اخبار اقتصادی و کریپتو:*\n\n"
message += "\n".join(headlines)
message += "\n\nمنبع: منابع معتبر جهانی | ارسال خودکار"

bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
