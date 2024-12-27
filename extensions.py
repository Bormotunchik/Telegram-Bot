import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException(f'Невозможно конвертировать одинаковые валюты: {base}.')
        
        url = f'https://api.exchangerate-api.com/v4/latest/{base}'
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException('Ошибка при получении данных с API.')

        data = response.json()
        if quote not in data['rates']:
            raise APIException(f'Валюта {quote} не найдена.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Некорректное количество: {amount}.')

        rate = data['rates'][quote]
        total_amount = rate * amount
        return total_amount
