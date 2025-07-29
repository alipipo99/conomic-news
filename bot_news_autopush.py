import os
import requests
from telegram import Bot
from datetime import datetime
from googletrans import Translator

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

bot = Bot(token=bot_token)
translator = Translator()

sources = [
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",  # CNBC Top News
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",  # WSJ Markets
    "https://www.investing.com/rss/news_25.rss",  # Investing.com Economics
    "https://cointelegraph.com/rss",  # Cointelegraph Crypto
    "https://www.theblock.co/rss",  # The Block
    "https://www.coindesk.com/arc/outboundfeeds/rss/"  # Coindesk
]

def fetch_rss_entries(url):
    import feedparser
    return feedparser.parse(url).entries[:10]

def format_news():
    headlines = []
    for src in sources:
        try:
            entries = fetch_rss_entries(src)
            for entry in entries[:2]:
                translated = translator.translate(entry.title, dest='fa').text
                date = datetime.utcnow().strftime('%Y-%m-%d')
                headlines.append(f"📰 {translated}
🌍 {entry.link}
📅 {date}")
        except Exception as e:
            headlines.append(f"⚠️ خطا در خواندن منبع: {src}")

    return "\n\n".join(headlines[:10])

def send_news():
    msg = format_news()
    full_msg = f"📢 *۱۰ خبر مهم اقتصادی و کریپتویی*

{msg}"
    bot.send_message(chat_id=chat_id, text=full_msg, parse_mode='Markdown')

if __name__ == "__main__":
    send_news()