from telebot import types
import telebot
from func import *
Host = '127.0.0.1'
User = 'postgres'
Password = 'As720aS1'
db_name = 'momo'

TOKEN = '5091571007:AAFQcsQ3UPJ427z-FyIlLY0Pi7pGpPYfLT0'

bot = telebot.TeleBot(TOKEN)

p_code = 0
corral_num = 0


stall = {'corral': 0, 'animal': 0}
animal = {'name': '', 'sex': '', 'age': 0, 'animal_type': 0, 'corral': 0}


@bot.message_handler(content_types=['text'])
def main(message):
    for i in range(message.id, -1, -1):
        try:
            bot.delete_message(message.chat.id, i)
        except Exception as ex:
            break
    global p_code, stall
    if message.text == 'Добавить загон' and not(p_code):
        bot.send_message(
            message.chat.id, 'Введите номер вида животных обитающего в нём', reply_markup='')
        p_code = 2
    elif message.text == 'Добавить вид животных' and not(p_code):
        bot.send_message(
            message.chat.id, 'Какой это вид животных?', reply_markup='')
        p_code = 4  
    elif message.text == 'Добавить стойло' and not(p_code):
        stall = {'corral': 0}
        bot.send_message(
            message.chat.id, 'Номер загона с этим стойлом', reply_markup='')
        p_code = 6
    elif message.text == 'Добавить животное' and not(p_code):
        bot.send_message(
            message.chat.id, 'Как зовут животное?', reply_markup='')
        p_code = 9
    elif message.text == 'Дропнуть БД' and not(p_code):
        DROP(bot, message)
    elif message.text == 'Список животных' and not(p_code):
        get_animals(bot, message)
    elif message.text == 'Список загонов' and not(p_code):
        get_corrals(bot, message)
    elif message.text == 'Список стойл' and not(p_code):
        get_stalls(bot, message)
    elif message.text == 'Список видов животных' and not(p_code):
        get_animal_types(bot, message)

    elif p_code == 0:
        makup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Добавить загон')
        item2 = types.KeyboardButton('Добавить вид животных')
        item3 = types.KeyboardButton('Добавить стойло')
        item4 = types.KeyboardButton('Добавить животное')
        item5 = types.KeyboardButton('Список животных')
        item6 = types.KeyboardButton('Список загонов')
        item7 = types.KeyboardButton('Список стойл')
        item8 = types.KeyboardButton('Список видов животных')
        item9 = types.KeyboardButton('Дропнуть БД')
        makup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)
        bot.send_message(message.chat.id, 'Что делать?', reply_markup=makup)

    elif p_code == 2:   
        try:
            create_corral(int(message.text), message, bot)
            p_code = 0
        except ValueError:
            bot.send_message(str(message.chat.id), 'Введите целое число')
        

    elif p_code == 4:
        if not(check_animal_type(message.text)):
            create_animal_type(message.text, message, bot)
        else:
            bot.send_message(message.chat.id, 'Ой-ёй, да этот вид уже есть\n\
Отправьте что-нибудь для продолжения', reply_markup='')
        p_code = 0        

    elif p_code == 6:
        try:
            if check_corral(int(message.text)):
                stall['corral'] = message.text
                bot.send_message(
                    message.chat.id, 'Номер животного в этом стойле', reply_markup='')
                p_code = 7
            else:
                error_corral(message, bot)
                p_code = 0
        except ValueError:
            bot.send_message(
                message.chat.id, 'Введите целое число', reply_markup='')

    elif p_code == 7:
        try:
            if check_animal(int(message.text)):
                stall['animal'] = int(message.text)
                create_stall(stall,  message, bot)
            else:
                error_animal(message, bot)
        except ValueError:
            pass
        p_code = 0
        

    elif p_code == 9:
        animal['name'] = message.text
        bot.send_message(
            message.chat.id, 'Какого пола животное?', reply_markup='')
        p_code = 10

    elif p_code == 10:
        animal['sex'] = message.text
        bot.send_message(
            message.chat.id, 'Сколько лет животному?', reply_markup='')
        p_code = 11

    elif p_code == 11:
        try:
            animal['age'] = int(message.text)
            bot.send_message(
                message.chat.id, 'Какого вида животное?(номер вида)', reply_markup='')
            p_code = 12
        except ValueError:
            bot.send_message(
                message.chat.id, 'Введите целое число', reply_markup='')

    elif p_code == 12:
        try:
            if check_animal_type(str(int(message.text))):
                animal['animal_type'] = message.text
                bot.send_message(   
                    message.chat.id, 'В каком оно загоне?', reply_markup='')
                p_code = 13
            else:
                error_animal_type(message.text, bot, message)
                p_code = 0
        except ValueError:
            bot.send_message(
                message.chat.id, 'Введите целое число', reply_markup='')

    elif p_code == 13:
        try:
            k = True
            animal['corral'] = int(message.text)
            for i in which_corral():
                if i[0] == animal['corral']:
                    break
            else:
                k = False
            if k:
                #if check_corral(str(int(animal['corral']))):
                if check_corral(str(int(1))):
                    create_animal(animal, message, bot)
                else:
                    bot.send_message(
                        message.chat.id, 'Ошибка\nВид животного не соответствует виду животных в загоне\nВыберете другой загон\nОтправте что-нибудь для продолжения', reply_markup='')
            else:
                error_corral(message, bot)
            p_code = 0
        except ValueError:
            bot.send_message(
                message.chat.id, 'Введите целое число', reply_markup='')


bot.polling()
