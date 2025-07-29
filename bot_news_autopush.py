import os
import requests
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

NEWS_SOURCES = [
    "https://www.cnbc.com/world/?region=world",
    "https://www.bloomberg.com",
    "https://www.tradingeconomics.com",
    "https://www.coindesk.com",
    "https://cointelegraph.com",
    "https://www.theblock.co",
    "https://finance.yahoo.com"
]

def fetch_headlines():
    headlines = []
    for url in NEWS_SOURCES:
        try:
            response = requests.get(f"https://api.codetabs.com/v1/proxy/?quest={url}")
            if response.status_code == 200 and "<title>" in response.text:
                title = response.text.split("<title>")[1].split("</title>")[0]
                translated = GoogleTranslator(source="en", target="fa").translate(title)
                headlines.append(f"📰 {translated}")
        except Exception as e:
            headlines.append(f"❌ خطا در خواندن {url}")
    return "\n".join(headlines)

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except:
        pass

if __name__ == "__main__":
    news = fetch_headlines()
    message = f"📡 آخرین اخبار اقتصادی و کریپتو:\n\n{news}\n\nمنبع: منابع معتبر جهانی | ارسال خودکار"
    send_to_telegram(message)