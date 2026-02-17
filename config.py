import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# Словарь валют: оставляем и русские, и англ названия для удобства
CURRENCIES = {
    'рубль': 'RUB',
    'доллар': 'USD',
    'евро': 'EUR',
    'rub': 'RUB',
    'usd': 'USD',
    'eur': 'EUR'
}