import requests
import json
from config import CURRENCIES

# 1. Собственное исключение
class APIException(Exception):
    pass

# 2. Класс для работы с API
class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        # Проверка, что введены корректные названия валют
        if base not in CURRENCIES:
            raise APIException(f'Не удалось обработать валюту {base}')
        if quote not in CURRENCIES:
            raise APIException(f'Не удалось обработать валюту {quote}')

        # Проверка на совпадение валют
        if base == quote:
            raise APIException(f'Нельзя перевести одинаковые валюты {base}!')

        # Проверка, что количество — это число
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        # Отправка запроса к API
        try:
            url = f'https://api.exchangerate-api.com/v4/latest/{CURRENCIES[base]}'
            response = requests.get(url)
            data = json.loads(response.text)
        except requests.exceptions.RequestException:
            raise APIException('Ошибка при запросе к API. Проверьте интернет-соединение.')

        # Парсинг ответа и расчет
        rate = data['rates'][CURRENCIES[quote]]
        converted_amount = rate * amount

        return converted_amount