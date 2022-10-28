from dotenv import load_dotenv, find_dotenv
import os
 
load_dotenv(find_dotenv())
 

url = 'https://lk.sut.ru/cabinet'

driver = 'D:\\Projects\\UniBot\\required\\chromedriver.exe'
TokenBot = os.getenv('TOKEN')

bonch = {
	'email': os.getenv('EMAIL'),
	'pass': os.getenv('PASS_LK')
}

mail = {
	'email': os.getenv('EMAIL'),
	'pass': os.getenv("PASS_MAIL")  # Пароль из 'Пароли Приложений' в Yandex ID
}

schedule = ( # Время начала 'занятий' бонча
	'08:50',
	'10:35',
	'12:50',
	'14:35',
	'16:20',
	'18:05',
)

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

