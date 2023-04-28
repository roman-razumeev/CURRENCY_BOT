from dotenv import load_dotenv
import os

load_dotenv()

# Getting token
TOKEN = os.getenv('TOKEN')

# List of currencies
keys = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'фунт': 'GBP',
}