import requests
from config import CURRENCIES


class APIException(Exception):
    """Класс для обработки ошибок пользователя и API"""
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        # 1. Проверяем наличие валют в нашем словаре
        if base not in CURRENCIES:
            raise APIException(f'Валюта "{base}" не найдена. Список: /values')

        if quote not in CURRENCIES:
            raise APIException(f'Валюта "{quote}" не найдена. Список: /values')

        # 2. Проверяем логику (нельзя менять доллар на доллар)
        if base == quote:
            raise APIException(f'Нельзя перевести {base} в {base}. Выберите разные валюты.')

        # 3. Валидация числа
        try:
            amount_val = float(amount.replace(',', '.'))  # На случай, если введут "10,5"
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        # 4. Запрос к API
        try:
            base_ticker = CURRENCIES[base]
            quote_ticker = CURRENCIES[quote]

            url = f'https://api.exchangerate-api.com/v4/latest/{base_ticker}'
            response = requests.get(url, timeout=10)  # Добавляем таймаут, чтобы бот не завис

            # Проверяем, что сервер ответил успешно
            if response.status_code != 200:
                raise APIException('Сервер API временно недоступен.')

            data = response.json()  # Питонический способ парсинга JSON

            rate = data['rates'].get(quote_ticker)
            if not rate:
                raise APIException(f'Не удалось получить курс для {quote}')

            return rate * amount_val

        except requests.exceptions.RequestException as e:
            raise APIException(f'Ошибка сети: {e}')