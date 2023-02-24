import telebot
from telebot import TeleBot
from tok import keys
from tok import TOKEN

from extensions import ConvertionException, CryptoConverter

bot: TeleBot = telebot.TeleBot(TOKEN)

# первые команды
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Приветсвую, {message.chat.username}, это бот обменник валют, следуйте моим сообщениям")
    text = '💵 Нажми на /valuta что бы увидеть список валют 💵\n'
    bot.reply_to(message, text)


# ЧАСТЬ 1

#  выводим на экран список операций и все актуальные  курсы
@bot.message_handler(commands=['valuta'])
def operations(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key))
    text = 'Напиши команду в формате:\n <из какой валюты переводим> <в какую валюту> <количество валюты>'
    bot.reply_to(message, text)

# ЧАСТЬ 2
# Обработка валюты пользователя
@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        message.text= message.text.lower()  #Если пользователь ввел какие то буквы большие, то выравниваем
        values = message.text.split(' ')
        quote, base, amount = values
        total_base=CryptoConverter.convert(quote, base, amount)
        amount = float(amount)
        total_base = float(total_base)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя{e}')
    except Exception as e:
        if len(values) != 3:
            bot.reply_to(message,'Слишком много параметров, измените запрос')
        else:
            bot.reply_to(message, f'Не удалось обработать команду\n{e} \n 💵 Нажми на /valuta что бы увидеть список валют 💵')
    else:
        if amount<0:                                                    #Проверяем что пользователь ввел не отрицательное значение
            bot.reply_to(message,'Вы ввели отрицательное значение')
        else:
            text = f'Цена {amount} {quote} в {base} = {total_base*amount}'
            bot.send_message(message.chat.id, text)
       




# Ответ на картинку
@bot.message_handler(content_types=['photo'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Присылайте, пожалуйства, котиков. Люблю котиков. Мур😸')

# Ответ на аудио
@bot.message_handler(content_types=['voice'])
def handle_docs_audio(message):
    bot.reply_to(message, 'Пробовали заниматься вокалом? Думаю, что у вас получится')


# Ответ на анимацию
@bot.message_handler(content_types=['animation'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, '🤪')


# Ответ на стикер
@bot.message_handler(content_types=['sticker'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, '🐙')


# Ответ на видео
@bot.message_handler(content_types=['video'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'NICE vidos')

bot.polling(none_stop=True)
