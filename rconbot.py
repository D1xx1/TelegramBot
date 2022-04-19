import telebot
import settings
import os

from mcrcon import MCRcon

bot = telebot.TeleBot(settings.token)

@bot.message_handler(content_types=['text'])
def donate(message):
    if message.text == '/donate':
        bot.send_message(message.from_user.id, "Введите ваш ник на сервере и желаемый уровень\nНапример: Username\n1...5")
        bot.register_next_step_handler_by_chat_id(message.chat.id, get_info)
    else:
        bot.send_message(message.from_user.id, 'Напишите /donate')
    
def get_info(message):          #Этот куссок кода создаёт файл с записью данных.
        nick_level = list(message.text.split('\n'))
        if len(nick_level) == 2:
            bot.send_message(message.from_user.id, f'Ник: {nick_level[0]}. Желаемый уровень: {nick_level[1]}')
            userID = message.from_user.id
            if not os.path.isdir('UserData'):
                os.mkdir('UserData')
            prevDir = os.getcwd()
            os.chdir('UserData')
            data = open('userinfo.txt','w')
            data.write(nick_level[1]+'\n'+nick_level[0]+'\n'+settings.level[int(nick_level[1])])
            data.close()
            if os.path.isfile(f'{userID}.txt'):
                os.remove(f'{userID}.txt')
            os.rename('userinfo.txt',f'{userID}.txt')
            os.chdir(prevDir)
            bot.send_message(message.from_user.id, 'Ожидание оплаты. Напишите /check для проверки.')
            print(userID, 'Запись создана.')
        else:
            bot.send_message(message.from_user.id, f'Ошибка ввода. Попробуйте снова.')
            bot.register_next_step_handler_by_chat_id(message.chat.id, get_info)



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