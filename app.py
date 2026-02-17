import telebot
from config import TOKEN, CURRENCIES
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = (
        'Привет! 👋 Я бот для конвертации валют.\n\n'
        'Отправь сообщение в формате:\n'
        '*<валюта 1> <валюта 2> <количество>*\n\n'
        'Пример: `доллар рубль 100`\n\n'
        'Список валют: /values'
    )
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    # Питонический способ сборки строк из списка (редакция от 01.2026)
    currencies_list = '\n'.join([f'• {c}' for c in CURRENCIES.keys()])
    text = f'Доступные валюты:\n{currencies_list}'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def handle_text(message: telebot.types.Message):
    try:
        parts = message.text.lower().split()

        if len(parts) != 3:
            raise APIException('Нужно 3 параметра: <валюта1> <валюта2> <количество>')

        base, quote, amount = parts
        converted_amount = CurrencyConverter.get_price(base, quote, amount)

        # Делаем результат более заметным с Markdown
        text = f'✅ *{amount}* {base} = *{round(converted_amount, 2)}* {quote}'
        bot.send_message(message.chat.id, text, parse_mode='Markdown')

    except APIException as e:
        bot.reply_to(message, f'⚠️ Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'🛠 Ошибка сервера:\n{e}')

if __name__ == '__main__':
    bot.polling(none_stop=True)