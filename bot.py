import os
import requests
from telegram import Bot
from datetime import datetime
from news_fetcher import get_translated_news

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

def send_news():
    news_items = get_translated_news()
    if not news_items:
        return
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    header = f"📰 *Economic & Crypto News Update*
🕒 {now}

"
    message = header + "

".join(news_items)
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

if __name__ == "__main__":
    send_news()
