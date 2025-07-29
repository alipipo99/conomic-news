import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import feedparser
from deep_translator import GoogleTranslator
from telegram import Bot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

RSS_FEEDS = [
    ("https://feeds.a.dj.com/rss/RSSMarketsMain.xml", "Wall Street Journal"),
    ("https://www.cnbc.com/id/100003114/device/rss/rss.html", "CNBC"),
    ("https://cointelegraph.com/rss", "Cointelegraph"),
    ("https://www.investing.com/rss/news_25.rss", "Investing.com"),
    ("https://finance.yahoo.com/news/rssindex", "Yahoo Finance")
]

def translate_text(text):
    try:
        return GoogleTranslator(source='auto', target='fa').translate(text)
    except:
        return text

async def main():
    headlines = []
    for url, source in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                title = feed.entries[0].title
                translated = translate_text(title)
                headlines.append(f"📰 {translated} ({source})")
            else:
                headlines.append(f"⚠️ خطا در دریافت از {source}")
        except Exception as e:
            headlines.append(f"⚠️ خطا در دریافت از {source}")

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    text = f"📡 آخرین اخبار اقتصادی و کریپتو - {now} (UTC):\n\n" + "\n".join(headlines)
    text += "\n\nمنبع: منابع معتبر جهانی | ارسال خودکار"

    await bot.send_message(chat_id=CHAT_ID, text=text)

if __name__ == "__main__":
    asyncio.run(main())
