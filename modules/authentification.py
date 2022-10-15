from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent as ua
import time
from datetime import datetime
import schedule

import sys
sys.path.insert(0, '../cfg')

import config as cfg

#-------------------------------------------------------------------
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
	StartLesson()



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
