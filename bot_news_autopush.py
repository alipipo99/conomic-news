import os
import asyncio
import logging
import feedparser
import requests
from datetime import datetime
from deep_translator import GoogleTranslator
from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

# منابع خبری معتبر همراه با RSS
RSS_FEEDS = [
    ("https://feeds.a.dj.com/rss/RSSMarketsMain.xml", "Wall Street Journal"),
    ("https://www.investing.com/rss/news_25.rss", "Investing.com"),
    ("https://www.cnbc.com/id/100003114/device/rss/rss.html", "CNBC"),
    ("https://www.bloomberg.com/feed/podcast/etf-report.xml", "Bloomberg"),
    ("https://www.tradingeconomics.com/united-states/rss.aspx?symbol=united-states", "TradingEconomics"),
    ("https://cointelegraph.com/rss", "Cointelegraph"),
    ("https://www.theblock.co/feeds/rss", "The Block"),
    ("https://www.lookonchain.com/feed/", "Lookonchain")
]

async def fetch_and_translate():
    headlines = []
    for url, source in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                title = feed.entries[0].title
                translated = GoogleTranslator(source='auto', target='fa').translate(text=title)
                headlines.append(f"\U0001F4F0 {translated} ({source})")
            else:
                headlines.append(f"⚠️ خطا در دریافت از {source}")
        except Exception as e:
            headlines.append(f"⚠️ خطا در دریافت از {source}")
            logging.warning(f"Error fetching from {source}: {e}")
    return headlines

async def send_news():
    headlines = await fetch_and_translate()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    text = f"\U0001F4E1 آخرین اخبار اقتصادی و کریپتو - {now} (UTC):\n\n" + "\n".join(headlines) + "\n\nمنبع: منابع معتبر جهانی | ارسال خودکار"
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)

if __name__ == "__main__":
    asyncio.run(send_news())
