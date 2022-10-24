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
			counter = log['Count']
			if counter < 1 :
				bot.send_message(message.from_user.id, 'Ничего не найдено...')
			else:
				info_with_files = AT.GetFiles(log)
				#print(info_with_files)
				#print(log)
				for i in range(counter):
					sms = 'Файлы Группы.'
					if info_with_files[i][0]['SMS_or_FILE']:
						sms = 'ЛК Сообщения.'
					file = ''
					if info_with_files[i][0]['HasFile']:
						file = f'\n\nФайл : {(info_with_files[i][-1])}'
					bot.send_message(message.from_user.id, (f'{sms}\n{info_with_files[i][0]["Text"]}\n\nНаличие файла: {True_OR_False[info_with_files[i][0]["HasFile"]]} \nПолучено от: {info_with_files[i][0]["From"]} \nВремя получения : {info_with_files[i][0]["Date"]}{file}'))
		case _:
			bot.send_message(message.from_user.id, 'Не распознаю команду')

bot.polling(none_stop = True, interval = 0)
