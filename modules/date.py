import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent as ua
import datetime as dt

import sys
sys.path.insert(0, '../cfg')

import config as cfg

def WhatDay(day = False, week = False):
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
	result = 1
	if day:
		date_sec = dt.date(2001, 1, 1) # Понедельник 2001-го года

		result = int(str(date - date_sec).split()[0]) % 7 + 1
	if week:
		date_sec = dt.date(2022, 8, 29) # Первая неделя семестра

		result = int(str(date - date_sec).split()[0]) // 7 + 1

	return result

def toNormalTime(time = None):
	if time == None:
		time = dt.datetime.now()
		return int(time.hour*60*60) + int(time.minute*60) + int(time.second)
	else:
		time = time.split(':')
		return int(time[0])*60*60 + int(time[1])*60 + int(time[2])

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

def PairsToday(name = False):
	session = requests.Session()

	fake = ua().google
	headers = {'User-Agent': fake}

	params = {
	 	'schet': '205.2223/1',
		'type_z': 1,
		'faculty': 50029,
		'kurs': 2,
		'group': 54865,
		'ok': 'Показать',
		'group_el': 0
	}

	url = 'https://cabinet.sut.ru/raspisanie_all_new'
	r = requests.post(url, headers = headers, params = params)
	site = BS(r.text, 'lxml')

	st = []

	week = WhatDay(week = True)
	for i in site.find_all(weekday = WhatDay(day = True)):
		str = i.find('span', attrs = {'class':'weeks'}).text

		x = '(),н*д'
		for j in x:
			str = str.replace(j, '')
		str = str.split()

		for num in str:
			if int(num) == week:
				if name:
					st.append(i.text[:i.text.find('\n'):])	
				else:
					if i['pair'] == '87':	
						st.append(4)
					else:
						st.append(int(i['pair']) - 1)			
	return st


if __name__ == '__main__':
	print('\n'.join(PairsToday(name = True)), '\n', PairsToday())
# print(PairsToday())
#r = session.get('https://lk.sut.ru/cabinet/?login=yes', headers = headers)
#site = BS(r.text, 'html.parser')
#print(site)

#logurl = 'https://lk.sut.ru/cabinet/lib/autentificationok.php'
#log = site.post(logurl, data = inputs)
#log_bs = BS(log.content, 'html.parser')