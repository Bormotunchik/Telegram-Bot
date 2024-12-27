import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Введите данные в формате: <валюта> <валюта для конвертации> <количество>.\n"
                          "Например: доллар рубль 100.\n"
                          "Используйте команду /values для получения списка доступных валют.")

@bot.message_handler(commands=['values'])
def values(message):
    bot.reply_to(message, "Доступные валюты:\n- доллар\n- евро\n- рубль")

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неверное количество параметров. Используйте формат: <валюта> <валюта для конвертации> <количество>.')

        base, quote, amount = values
        total_amount = CurrencyConverter.get_price(base, quote, amount)

        result = f'{amount} {base} равняется {total_amount} {quote}.'
        bot.reply_to(message, result)

    except APIException as e:
        bot.reply_to(message, f'Ошибка: {e}')

if __name__ == '__main__':
    bot.polling(none_stop=True)
