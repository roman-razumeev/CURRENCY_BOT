import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter


# Telegram bot object creation
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    ''' Start function. '''

    text = 'Привет! Я Бот-Конвертер валют и я могу:  \n ' \
           '- Показать список доступных валют через команду /values\n ' \
           '- Вывести конвертацию валюты через команду <имя валюты> ' \
           '<в какую валюту перевести> <количество переводимой валюты>\n ' \
           '- Напомнить, что я могу через команду /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    ''' Help function. '''

    text = 'Чтобы начать конвертацию, введите команду боту в следующем ' \
           'формате: \n<имя валюты> <в какую валюту перевести> <количество ' \
           'переводимой валюты>\nЧтобы увидеть список всех доступных валют, ' \
           'введите команду\n/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    ''' To output the list of currencies function. '''

    text = 'Доступные валюты:'

    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    ''' Checking numbers of parametrs and output a current exchange rate by
    running get_price method. '''

    try:
        # Checking numbers of parametrs
        values = message.text.split(' ')
        if len(values) > 3:
            raise APIException('Слишком много параметров.\n'
                               'Введите команду или 3 параметра')
        elif len(values) < 3:
            raise APIException('Слишком мало параметров.\n'
                               'Введите команду или 3 параметра')
        # If param numbers is ok then get them
        quote, base, amount = values
        # and run converter
        total_base = CryptoConverter.get_price(quote, base, amount)

    # To output errors
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    # To output exchange rate
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)

# Run bot
bot.polling()
