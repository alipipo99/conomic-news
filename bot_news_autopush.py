import os
import requests
import feedparser
from deep_translator import GoogleTranslator
from telegram import Bot
from dotenv import load_dotenv

# بارگذاری اطلاعات از .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

# منابع خبری RSS
rss_sources = [
    ("https://www.cnbc.com/id/100003114/device/rss/rss.html", "CNBC"),
    ("https://cointelegraph.com/rss", "Cointelegraph"),
    ("https://www.theblock.co/rss.xml", "The Block"),
    ("https://www.lookonchain.com/feed", "Lookonchain")
]

def get_latest_news():
    headlines = []
    for url, source in rss_sources:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                raw_title = feed.entries[0].title
                translated = GoogleTranslator(source='auto', target='fa').translate(raw_title)
                headlines.append(f"\ud83d\udcf0 {translated} ({source})")
            else:
                headlines.append(f"\u26a0\ufe0f خبری دریافت نشد از {source}")
        except Exception as e:
            headlines.append(f"\u26a0\ufe0f خطا در دریافت از {source}")
    return headlines

def format_message():
    news_items = get_latest_news()
    message = "\ud83d\udcf1\u00a0آخرین اخبار اقتصادی و کریپتو:\n\n"
    message += "\n".join(news_items)
    message += "\n\nمنبع: منابع معتبر جهانی | ارسال خودکار"
    return message

def send_news():
    text = format_message()
    bot.send_message(chat_id=CHAT_ID, text=text)

if __name__ == "__main__":
    send_news()
