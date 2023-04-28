import requests
import json
from config import keys

# Exception class
class APIException(Exception):
    pass

# Converter class:
class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        ''' Checking errors in the parametrs and execute convertion. '''

        # Checking errors in 4 checks:
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')

        # Receive current exchange rate from the site
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym='
                         f'{quote_ticker}&tsyms={base_ticker}')

        # Convert to JSON format
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amount
