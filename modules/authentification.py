from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent as ua

import time
from datetime import datetime
import date
import schedule

import requests
from bs4 import BeautifulSoup as BS
import re

import sys
sys.path.insert(0, '../cfg')

import config as cfg

#-------------------------------------------------------------------
def GetFiles(mail = None):
	if mail == None:
		print('Just Test')
		mail = {0: {'Text': 'Сообщение: Тут большое сообщение', 'From': 'Кто-то Какой-то Палыч', 'HasFile': True, 'SMS_or_FILE': True, 'Date': 'Fri, 16 Oct 2022 12:26:56 +0300'}}
	#https://lk.sut.ru/project/cabinet/forms/files_group_pr.php
	browser = StartSite()
	browser.get('https://lk.sut.ru/project/cabinet/forms/files_group_pr.php')

	parsing = BS(browser.page_source, 'html.parser')
	
	pars_data = {}
	counter = 0
	for child_tr in parsing.find_all("tr", id=re.compile("^tr")):
		link = child_tr.find(href = True)
		if link:
			link = link['href']
		else:
			link = None

		t = child_tr.text.split()
		file = t[-2]
		if re.match('[а-яА-Я]', t[-2]):
			file = None
		x = f'{t[1]} {t[2]} {t[3]}'.strip() 
		info = [x, f'{t[4]} {t[5]}', file]
		pars_data.update({counter: {'Info': info, 'link': link}})
		counter += 1

	browser.get('https://lk.sut.ru/project/cabinet/forms/message.php')
	parsing = BS(browser.page_source, 'html.parser')

	for child_tr in parsing.find_all("tr", id=re.compile("^tr")):
		link = child_tr.find(href = True)
		if link:
			link = link['href']
		else:
			link = None

		t = child_tr.text.split()
		#print(t)
		# file = t[-2]
		# if re.match('[а-яА-Я]', t[-2]):
		# 	file = None
		x = f'{t[-4]} {t[-3]} {t[-2]}'.strip() 
		info = [x, f'{t[0]} {t[1]}']
		pars_data.update({counter: {'Info': info, 'link': link}})
		counter += 1

	#print(pars_data)
	result = []
	for i in range(mail['Count']):
		if mail[i]['HasFile']:
			for k in range(counter):
				#print(mail[i]['From'], pars_data[k]['Info'][0] ,mail[i]['From'] == pars_data[k]['Info'][0])
				if mail[i]['From'] == pars_data[k]['Info'][0]:
					#print(mail[i]['Date'], date.addTime(pars_data[k]['Info'][1], -60), date.addTime(pars_data[k]['Info'][1], 240))
					if mail[i]['Date'] > date.addTime(pars_data[k]['Info'][1], -60) and mail[i]['Date'] < date.addTime(pars_data[k]['Info'][1], 240):
						result.append([mail[i], pars_data[k]['link']])
				else:
					continue
		else:
			result.append([mail[i], None])
	#print(result)
	return result

def CheckButton(browser, timecounter = 0, file = None, justOnce = False):
	if not justOnce:
		shutdown = file.read()
		# Считывание данных с файла и переход к первой строке, ибо при считывании в первый раз, переходит на след строки, которые не считались.
		file.seek(0) 
		if shutdown == 'Stop':
			#print('Принудительное завершение работы модуля...')
			return 'Модуль остановлен'

		if timecounter >= 6300:
			#print('Кнопку не дали / произошла ошибка')
			return 'Кнопку не дали...'
		
	#---------------------------------------------------------------
	uch = browser.find_element(By.XPATH, '//*[@id="heading1"]/h5/div').click() # (By.XPATH, '//*[@id="heading1"]/h5/div')
	pasp = browser.find_element(By.XPATH, '//*[@id="menu_li_6118"]').click() # (By.XPATH, '//*[@id="menu_li_6118"]')
	
	time.sleep(1)

	try:
		tryclick = browser.find_element(By.LINK_TEXT, 'Начать занятие') #  //*[@id="knop604797"]/a
		# actions = AC(browser)
		# actions.move_to_element(tryclick)
		# actions.perform()
	except:
		#print('Попытка в : ', datetime.now())
		if justOnce:
			return 'Кнопку не дали...'

		if timecounter >= 6000:
			timecounter += 300
			time.sleep(300)
		else:
			timecounter += 600
			time.sleep(600)
		browser.refresh()
		CheckButton(browser, timecounter, file)
	else:
		#print(tryclick)
		tryclick.click()
		#print(f'Кнопка нажата : {datetime.now()}')
		return 'Готово!'

#-------------------------------------------------------------------
def StartSite():
	fake = ua().chrome

	# Выставление параметров браузера
	options = Options()
	for i in cfg.options:
		options.add_argument(i)

	options.add_argument(f'user-agent={fake}')
	browser = webdriver.Chrome(service = Service(cfg.driver), options = options) # Запуск ГуглХрома
	browser.get(cfg.url)

	# Взаимодействие с элементами по XPATH
	email = browser.find_element(By.XPATH, '//*[@id="users"]').send_keys(cfg.bonch['email']) 
	password = browser.find_element(By.XPATH, '//*[@id="parole"]').send_keys(cfg.bonch['pass'])
	login = browser.find_element(By.XPATH, '//*[@id="logButton"]').click()

	time.sleep(1)

	return browser

#-------------------------------------------------------------------
def StartLesson(fromSchedule = False, justOnce = False):
	browser = StartSite()
	toDo = ''

	if justOnce:
		toDo = CheckButton(browser, justOnce = True)
	else:
	# Файл требующийся для замены 'переменной' в realtime, чтобы принудительно остановить работу программы
		with open('../required/check_file.txt', 'r') as file:
			CheckButton(browser, 0, file)
	
	#---------------------------------------------------------------
	# file = open('test.txt', 'w').close() # Сброс файла
	time.sleep(1)
	
	browser.quit() # Закрытие браузера
	if fromSchedule:
		return schedule.CancelJob
	return toDo
#-------------------------------------------------------------------
if __name__ == '__main__':
	StartLesson(justOnce = True)


# //*[@id="knop604816"] -- span element button
# //*[@id="knop604816"]/a -- a element button 'Начать занятие'
# <a onclick="open_zan(604816,31);">Начать занятие</a>
# <span id="knop604816"><a onclick="open_zan(604816,31);">Начать занятие</a></span>
# После нажатия меняется на <span id="knop604816">10:50</span> 
# //*[@id="knop604816"]

#//*[@id="knop604821"]
#<span id="knop604821"><a onclick="update_zan(604821);">Кнопка появится в 12:50. Обновить.</a></span>
#<a onclick="update_zan(604821);">Кнопка появится в 12:50. Обновить.</a>
#//*[@id="knop604821"]/a
