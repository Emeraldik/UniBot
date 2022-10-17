import telebot

import sys
sys.path.insert(0, 'cfg')

import config as cfg

sys.path.insert(0, 'modules')

import launch
import authentification as AT
import mail

#import subprocess as sp

True_OR_False = {
	True : 'Да',
	False : 'Нет',
}

def file_module(text):
	with open('test.txt', 'w') as file:
		file.write(text)

bot = telebot.TeleBot(cfg.TokenBot)

# @bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['text'])
def get_Command(message):
	match message.text: 
		case 'Stop':
			bot.send_message(message.from_user.id, 'Останавливаем работу модуля...')
			file_module('Stop')
		case 'Start':
			bot.send_message(message.from_user.id, 'Запускаем работу модуля...')
			file_module(' ')
		case 'Click':
			bot.send_message(message.from_user.id, 'Принудительно нажимаю кнопку...')
			file_module(' ')
			toDo = AT.StartLesson(justOnce = True)
			bot.send_message(message.from_user.id, toDo)
		case 'Check Mail':
			bot.send_message(message.from_user.id, 'Отправляю запрос...')
			log = mail.CheckMail()
			if log['Count'] < 1 :
				bot.send_message(message.from_user.id, 'Ничего не найдено...')
			else:
				info_with_files = AT.GetFiles(log)
				print(info_with_files)
				print(log)
				# for i in range(log['Count']):
				# 	if log[i]['HasFile']:
				# 		bot.send_message(message.from_user.id, (info_with_files[i][-1]))
				# 	bot.send_message(message.from_user.id, (f'{log[i]["Text"]}\n\nНаличие файла: {True_OR_False[log[i]["HasFile"]]} \nПолучено от: {log[i]["From"]} \nВремя получения : {log[i]["Date"]}'))
		case _:
			bot.send_message(message.from_user.id, 'Не распознаю команду')

bot.polling(none_stop = True, interval = 0)
