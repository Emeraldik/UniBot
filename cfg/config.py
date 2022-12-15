from dotenv import load_dotenv, find_dotenv
import os
 
load_dotenv(find_dotenv())
 

url = 'https://lk.sut.ru/cabinet'

driver = 'D:\\Projects\\UniBot\\required\\chromedriver.exe'

TokenBot = os.getenv('TOKEN')
chat_ID = os.getenv('CHAT_ID')

bonch = {
	'email': os.getenv('EMAIL'),
	'pass': os.getenv('PASS_LK')
}

mail = {
	'email': os.getenv('EMAIL'),
	'pass': os.getenv("PASS_MAIL")  # Пароль из 'Пароли Приложений' в Yandex ID
}

schedule = { # Время начала 'занятий' бонча
	1:	'08:50',
	2:  '10:35',
	3:	'12:50',
	4:	'14:35',
	5:	'16:20',
	6:	'18:05',
	10: '14:50',
}

options = (
	'--no-sandbox', # Bypass OS security model
	'--disable-gpu', # applicable to windows os only
	'disable-infobars', # Отключает инфо
	'--disable-extensions', # Отключает расширения
	#'--window-size=800,600',
	'start-maximized', # Запускает браузер в fullscreen
	'--headless', # Браузер запустится в инвизе - пока что мешает работе 'Начать занятие'
	'--disable-blink-features=AutomationControlled' # Определение браузера как человека, а не робота (помогает для капчи) 
)

