import telebot
from config import *
from extensions import Converter, ApiExceptions


bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Добро пожаловать в конвертер валют! \n Введите запрос в формате USD RUB 100 \n " \
           "чтобы узнать цену 100 USD в RUB. \n Список поддерживаемых валют /values"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges:
        text = '\n'.join((text, i))
        text = ' - '.join((text, exchanges[i]))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, sym, amount = message.text.split()
    except ValueError as e:
        bot.reply_to('Не верное количество параметров')
    try:
        new_price = Converter.get_price(base, sym, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {sym} : {new_price}")
    except ApiExceptions as e:
        bot.reply_to(message, f'Ошибка в команде {e}')



bot.polling()