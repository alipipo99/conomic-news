import requests

sources = [
    ("https://www.cnbc.com/world/?region=world", "CNBC"),
    ("https://www.bloomberg.com/markets/economics", "Bloomberg"),
    ("https://www.yahoo.com/finance", "Yahoo Finance"),
    ("https://tradingeconomics.com/united-states/indicators", "TradingEconomics"),
    ("https://cointelegraph.com", "Cointelegraph"),
    ("https://www.theblock.co", "The Block"),
    ("https://www.lookonchain.com", "Lookonchain"),
]

def get_translated_news():
    # شبیه‌سازی اخبار برای تست
    return [
        "🇺🇸 شاخص هزینه مصرف شخصی آمریکا (PCE) روز پنج‌شنبه منتشر می‌شود. (منبع: Bloomberg)",
        "📉 اتریوم امروز به زیر 3800 دلار رسید. (منبع: Cointelegraph)",
        "🔔 بانک مرکزی آمریکا ممکن است تا پایان سال نرخ بهره را کاهش دهد. (منبع: CNBC)",
    ]
