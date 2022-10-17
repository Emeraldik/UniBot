import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent as ua
import datetime as dt

import sys
sys.path.insert(0, '../cfg')

import config as cfg

def WhatDay():
	# days = (
	# 	'Понедельник',
	# 	'Вторник',
	# 	'Среда',
	# 	'Четверг',
	# 	'Пятница',
	# 	'Суббота',
	# 	'Воскресенье',
	# )

	x = str(dt.datetime.today()).split()[0].split('-')

	date = dt.date(int(x[0]), int(x[1]), int(x[2]))
	date_sec = dt.date(2001, 1, 1) # Понедельник 2001-го года

	result = int(str(date - date_sec).split()[0]) % 7
	return result

def addTime(source, time_plus):
	format = "%d-%m-%Y %H:%M:%S"
	dt_object = dt.datetime.strptime(source, format)
	dt_object += dt.timedelta(seconds = time_plus)

	str = dt.datetime.strftime(dt_object, format)
	return str

def toNormalDate(data):
	#Fri, 07 Oct 2022 12:26:56 +0300
	raw = data.split()[1:-1]
	months = (
		'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jul', 'Jun', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
	)
	month = str(months.index(raw[1]) + 1)
	if int(month) < 10:
		month = '0' + month
	#07-10-2022 12:26:56
	return f'{raw[0]}-{month}-{raw[2]} {raw[-1]}'

def PairsToday():
	session = requests.Session()

	fake = ua().google
	headers = {'User-Agent': fake}

	params = {
	 	'schet': '205.2122/2',
		'type_z': 1,
		'faculty': 50029,
		'kurs': 1,
		'group': 54865,
		'ok': 'Показать',
		'group_el': 0
	}

	url = 'https://cabinet.sut.ru/raspisanie_all_new'
	r = requests.post(url, headers = headers, params = params)
	site = BS(r.text, 'html.parser')

	st = []

	for i in site.find_all(weekday = WhatDay() + 1):
		#print(i['pair'])
		if i['pair'] == '83':	
			st.append('2')
		else:
			st.append(i['pair'])

	result = [(int(i)-2) for i in sorted(list(set(st)))]
	return result

# print(PairsToday())
#r = session.get('https://lk.sut.ru/cabinet/?login=yes', headers = headers)
#site = BS(r.text, 'html.parser')
#print(site)

#logurl = 'https://lk.sut.ru/cabinet/lib/autentificationok.php'
#log = site.post(logurl, data = inputs)
#log_bs = BS(log.content, 'html.parser')