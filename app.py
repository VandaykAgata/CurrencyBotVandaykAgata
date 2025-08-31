import telebot
from config import TOKEN, CURRENCIES
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


# Обработчик команды /start и /help
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = (
        'Привет! 👋 Я бот для конвертации валют.\n\n'
        'Чтобы узнать цену, отправь сообщение в формате:\n'
        '**<имя валюты, которую переводим> <имя валюты, в которую переводим> <количество>**\n\n'
        'Например: `доллар рубль 100`\n\n'
        'Посмотреть доступные валюты: /values\n'
        'Помощь: /help'
    )
    bot.reply_to(message, text, parse_mode='Markdown')


# Обработчик команды /values
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for currency in CURRENCIES:
        text += f'• {currency}\n'
    bot.reply_to(message, text)


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message: telebot.types.Message):
    try:
        # Разделяем сообщение на три части
        parts = message.text.lower().split()

        # Проверка на корректное количество аргументов
        if len(parts) != 3:
            raise APIException(
                'Неправильное количество параметров. Используйте формат: <валюта1> <валюта2> <количество>')

        base, quote, amount = parts

        # Конвертация и отправка результата
        converted_amount = CurrencyConverter.get_price(base, quote, amount)

        # Формирование ответа
        text = f'{amount} {base} = {round(converted_amount, 2)} {quote}'
        bot.send_message(message.chat.id, text)

    except APIException as e:
        # Обработка собственных ошибок
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        # Обработка остальных ошибок
        bot.reply_to(message, f'Непредвиденная ошибка: {e}')


# Запуск бота
if __name__ == '__main__':
    print('Бот запущен. Чтобы остановить, нажмите Ctrl+C')
    bot.polling(none_stop=True)