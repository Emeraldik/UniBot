import imaplib as ilib
import email as EM
import config as cfg
from bs4 import BeautifulSoup as BS
#import datetime

import sys
sys.path.insert(0, '../cfg')

import config as cfg

sys.path.insert(0, '../modules')
import date as dt

def CheckMail():
	email = ilib.IMAP4_SSL('imap.yandex.ru')
	email.login(cfg.mail['email'], cfg.mail['pass']) #Авторизация в Yandex Mail через IMAP

	email.select('inbox') # Переход к 'Входящим'
	result, data = email.uid('search', 'UNSEEN', 'FROM "anketa@sut.ru"') # Собираем UID писем НЕПРОЧИТАННЫХ от СПбГУТ
	mails = data[0].split()
	counter = 0
	full_info = {}
	for i in mails:
		result, data = email.uid('fetch', i, '(RFC822)')
		#print('----------------')
		
		email_message = EM.message_from_bytes(data[0][1])
		#print(email_message['Date'])
		#print(email_message['Subject'])
		
		if email_message.is_multipart():
		   	mail_content = ''
		   	for part in email_message.get_payload():	
		   		if part.get_content_type() == 'text/plain':
		   			mail_content += part.get_payload()
		else:
		    mail_content = email_message.get_payload()
		
		soup = BS(mail_content, 'html.parser')
		text = soup.get_text()
		
		if 'Загружены файлы в личном кабинете' in text:
			SMS_or_FILE = False
		elif 'Уведомление о сообщении в ЛК СПбГУТ (отвечать ТОЛЬКО в ЛК)' in text:
			SMS_or_FILE = True

		HasFile = 'Прикрепленные файлы: смотрите в личном кабинете СПбГУТ.' in text
		if HasFile:
			text = text.replace('Прикрепленные файлы: смотрите в личном кабинете СПбГУТ.', '')

		start = text.find('Сообщение')
		end = text.find('Отправитель')
		fromwho = text.find('Отвечать необходимо в личном кабинете')
		
		info = {
			counter : {
				'Text' : text[start: end],
				'From' : text[end + 13: fromwho],
				'HasFile' : HasFile,
				'SMS_or_FILE' : SMS_or_FILE,
				'Date' : dt.toNormalDate(email_message['Date']),
			},
		}
		full_info.update(info)
		counter += 1
		
		#print(text[start : end])
		#print(f'From : {text[end + 13: fromwho]} \nHave file: {bool} \n SMS: {SMS_or_FILE}')

	count = {
		'Count' : counter
	}
	
	full_info.update(count)

	email.logout()
	return full_info
#   	anketa@sut.ru
