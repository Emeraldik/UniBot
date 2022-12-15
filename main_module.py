import telebot
import sys
import multiprocessing as mp

sys.path.insert(0, 'cfg')

import config as cfg

sys.path.insert(0, 'modules')

import launch
import authentification as AT
import mail

True_OR_False = {
  True: 'Да',
  False: 'Нет',
}


def file_module(text=' ', check=False, add=False):
	if check:
	    with open('D:/Projects/UniBot/required/check_file.txt', 'r') as file:
	      return file.read()
	else:
		if add:
			with open('D:/Projects/UniBot/required/check_file.txt', 'a') as file:
				file.write(text)
		else:
			with open('D:/Projects/UniBot/required/check_file.txt', 'w') as file:
				file.write(text)



bot = telebot.TeleBot(cfg.TokenBot)

@bot.message_handler(commands=['mail'])
def checkBOTMail(message=cfg.chat_ID):
  if message != cfg.chat_ID:
    user = message.from_user.id
    bot.send_message(user, 'Отправляю запрос...')
  else:
    user = cfg.chat_ID

  lst = mail.mail_BOT_request()
  print('lst = ', lst)
  if lst == 0:
    if message != cfg.chat_ID:
      bot.send_message(user, 'Ничего не найдено...')
  else:
    counter = lst[0]
    info_with_files = lst[1]
    for i in range(counter):
      sms = 'Файлы Группы.'
      if info_with_files[i][0]['SMS_or_FILE']:
        sms = 'ЛК Сообщения.'
      file = ''
      if info_with_files[i][0]['HasFile']:
        file = '\n\nФайл(ы) : ' + '\n\n'.join(
          info_with_files[i][-1][j]
          for j in range(len(info_with_files[i][-1])))
      bot.send_message(user, (
        f'{sms}\n{info_with_files[i][0]["Text"]}\n\nНаличие файла: {True_OR_False[info_with_files[i][0]["HasFile"]]} \nПолучено от: {info_with_files[i][0]["From"]} \nВремя получения : {info_with_files[i][0]["Date"]}{file}'
      ))


@bot.message_handler(commands=['click'])
def clickBOTLK(message):
  bot.send_message(message.from_user.id, 'Принудительно нажимаю кнопку...')
  toDo = AT.StartLesson(justOnce=True)
  bot.send_message(message.from_user.id, toDo)


@bot.message_handler(commands=['start_click'])
def start_clickBOTLK(message):
	global sched
	if file_module(check=True) != 'Stop':
		bot.send_message(message.from_user.id, 'Модуль уже запущен...')
	else:
		bot.send_message(message.from_user.id, 'Запускаем работу модуля...')
		file_module()
		if not sched.is_alive():
			sched = mp.Process(target=launch.StartSchedule)
			sched.start()


@bot.message_handler(commands=['stop_click'])
def stop_clickBOTLK(message):
	global sched
	if file_module(check=True) == 'Stop':
		bot.send_message(message.from_user.id, 'Модуль и так остановлен...')
	else:
		bot.send_message(message.from_user.id, 'Останавливаем работу модуля...')
		file_module('Stop')
		if sched.is_alive():
			sched.terminate()
    #launch.DeleteAllSchedule(stop=True)


@bot.message_handler(content_types=['text'])
def somethingBOTText(message):
  bot.send_message(message.from_user.id, 'Не распознаю команду')


def main():
  if file_module(check=True) != 'Stop':
  	file_module('')
  	global sched
  	sched = mp.Process(target=launch.StartSchedule)
  	sched.start()

  sched_mail = mp.Process(target=launch.StartSchedule_Mail).start()
  
  bot.polling(none_stop=True, interval=0)

if __name__ == '__main__':
  main()
