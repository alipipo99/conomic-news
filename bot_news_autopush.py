import os
import requests
import time
import telegram
from datetime import datetime
from bs4 import BeautifulSoup
from googletrans import Translator

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telegram.Bot(token=BOT_TOKEN)
translator = Translator()

def fetch_news():
    sources = [
        "https://www.cnbc.com/world/?region=world",
        "https://www.bloomberg.com/markets/economics",
        "https://www.tradingeconomics.com/",
        "https://www.coindesk.com/",
        "https://cointelegraph.com/"
    ]
    headlines = []

    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            titles = soup.find_all(['h2', 'h3'], limit=3)

            for title in titles:
                text = title.get_text().strip()
                if 10 < len(text) < 140:
                    translated = translator.translate(text, dest='fa').text
                    headlines.append(f"📰 {translated}")
        except Exception as e:
            print(f"Error fetching from {url}: {e}")

    return headlines

def send_news():
    headlines = fetch_news()
    if headlines:
        message = f"📡 *آخرین اخبار اقتصادی و کریپتو:*\n\n"
        message += "\n".join(headlines)
        message += "\n\n🕒 ارسال خودکار هر ۳ ساعت\n📎 منبع: CNBC، Bloomberg، Cointelegraph و سایر منابع جهانی"
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

if __name__ == "__main__":
    send_news()
