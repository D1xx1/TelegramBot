import telebot
import settings
from mcrcon import MCRcon
from telebot import types

bot = telebot.TeleBot(settings.token)

@bot.message_handler(content_types=['text'])
def donate(message):
    if message.text == '/donate':
        bot.send_message(message.from_user.id, "Введите ваш ник на сервере")
        bot.register_next_step_handler_by_chat_id(message.chat.id, get_nickname)
    else:
        bot.send_message(message.from_user.id, 'Напишите /donate')
    
def get_nickname(message):
    global nickname
    nickname = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_vip = types.InlineKeyboardButton(text='Уровень 1', callback_data='vip')
    keyboard.add(key_vip)
    key_prem = types.InlineKeyboardButton(text='Уровень 2', callback_data='prem')
    keyboard.add(key_prem)
    key_premplus = types.InlineKeyboardButton(text='Уровень 3', callback_data='premplus')
    keyboard.add(key_premplus)
    key_global = types.InlineKeyboardButton(text='Уровень 4', callback_data='global')
    keyboard.add(key_global)
    key_sponsor = types.InlineKeyboardButton(text='Уровень 5', callback_data='sponsor')
    keyboard.add(key_sponsor)
    bot.send_message(message.from_user.id, f'Ваш ник {nickname}. Укажите желаемый урвоень привилегии.', reply_markup=keyboard)
    bot.register_next_step_handler_by_chat_id(message.chat.id, callback_worker)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    mc = MCRcon(settings.ip, settings.password, port=25575)
    mc.connect()
    if call.data == "vip":
        mc.command(f'lp user {nickname} group set vip')
    if call.data == "prem":
        mc.command(f'lp user {nickname} group set prem')
    if call.data == "premplus":
        mc.command(f'lp user {nickname} group set premplus')
    if call.data == "global":
        mc.command(f'lp user {nickname} group set global')
    if call.data == "sponsor":
        mc.command(f'lp user {nickname} group set sponsor')
    mc.disconnect()

bot.polling(none_stop=True, interval=0, skip_pending=True)