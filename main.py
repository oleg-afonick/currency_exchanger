import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges, commands
import traceback

bot = telebot.TeleBot(TOKEN)

# Currency_super_bot - имя бота для поиска в телеграмме

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Вас приветствует бот перевода валют!\n\n'
    text += 'Список команд:\n'
    for i, k in enumerate(commands.items(), 1):
        text = '\n'.join((text, f'{i}. {k[0]} - {k[1]}'))
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['currency'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for i, k in enumerate(exchanges.keys(), 1):
        text = '\n'.join((text, f'{str(i)}. {k}'))
    text += '\n\nДля начала конвертации: /convert\n'
    text += '''\nВНИМАНИЕ!
При введении любых команд во время процесса конвертации
ВЫПОЛНЕНИЕ КОНВЕРТАЦИИ БУДЕТ ПРЕРВАНО!\n'''
    text += '\nДля просмотра списка доступных валют: /currency\n'
    text += 'Для перезапуска: /start'
    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def converter(message: telebot.types.Message):
    text = 'Введите валюту, из которой переводим: '
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, base_converter)

def base_converter(message: telebot.types.Message):
    base = message.text.strip()
    if base.lower() in list(commands.keys()):
        text = Convertor.stopping_conversion()
        bot.send_message(message.chat.id, text)
    elif base.lower() not in list(exchanges.keys()):
        text = 'Введена неизвестная валюта! Снова введите валюту, из которой переводим: '
        bot.reply_to(message, text)
        bot.register_next_step_handler(message, base_converter)
    else:
        text = 'Введите валюту, в которую переводим: '
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, sym_converter, base)


def sym_converter(message: telebot.types.Message, base):
    sym = message.text.strip()
    if sym.lower() in list(commands.keys()):
        text = Convertor.stopping_conversion()
        bot.send_message(message.chat.id, text)
    elif sym.lower() not in list(exchanges.keys()):
        text = 'Введена неизвестная валюта! Снова введите валюту, в которую переводим: '
        bot.reply_to(message, text)
        bot.register_next_step_handler(message, sym_converter, base)
    elif sym.lower() == base.lower():
        text = 'Введены одинаковые валюты! Снова введите валюту, в которую переводим: '
        bot.reply_to(message, text)
        bot.register_next_step_handler(message, sym_converter, base)
    else:
        text = 'Введите количество переводимой валюты: '
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, amount_converter, base, sym)


def amount_converter(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    if amount.lower() in list(commands.keys()):
        text = Convertor.stopping_conversion()
        bot.send_message(message.chat.id, text)
    elif not amount.isdigit():
        text = 'Введено не число! Снова введите количество переводимой валюты: '
        bot.reply_to(message, text)
        bot.register_next_step_handler(message, amount_converter, base, sym)
    else:
        text = 'Результат конвертации: '
        bot.send_message(message.chat.id, text)
        try:
            answer = Convertor.get_price(base, sym, amount)
        except APIException as e:
            bot.reply_to(message, f"Ошибка в команде:\n{e}")
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
        else:
            bot.send_message(message.chat.id, answer)


bot.polling()
