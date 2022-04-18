import telebot
import settings
import os

from mcrcon import MCRcon

bot = telebot.TeleBot(settings.token)

def record_user_data(prise, selectLevel):
    if not os.path.isdir('userdata'):
        os.mkdir('UserData')
    prevDir = os.getcwd()
    os.chdir('UserData')
    data = open('Data.txt','w')
    data.write(selectLevel +' '+ prise)
    data.close()
    if os.path.isfile(f'{nickname}.txt'):
        os.remove(f'{nickname}.txt')
    os.rename('Data.txt',f'{nickname}.txt')
    os.chdir(prevDir)

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
    bot.send_message(message.from_user.id, f'Ваш ник {nickname}. Укажите желаемый урвоень привилегии.')
    bot.register_next_step_handler_by_chat_id(message.chat.id, get_level)

def get_level(message):
        selectLevel = message.text
        if selectLevel == '1' or selectLevel == '2' or selectLevel == '3' or selectLevel == '4' or selectLevel == '5':
            prise = settings.level[int(selectLevel)]
            record_user_data(prise, selectLevel)
        else:
            bot.send_message(message.from_user.id, 'Введите число 1...5')
            bot.register_next_step_handler_by_chat_id(message.chat.id, get_level)

'''mc = MCRcon(settings.ip, settings.password, port=25575)
mc.connect()
mc.command(f'lp user {nickname} group set vip')
mc.command(f'lp user {nickname} group set prem')
mc.command(f'lp user {nickname} group set premplus')
mc.command(f'lp user {nickname} group set global')
mc.command(f'lp user {nickname} group set sponsor')
mc.disconnect()
'''
bot.polling(none_stop=True, interval=0, skip_pending=True)