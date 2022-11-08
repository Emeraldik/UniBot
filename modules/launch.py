import schedule
#import requests
import authentification as auth
import time
import date as dt

import sys
sys.path.insert(0, '../cfg')

import config as cfg

def ChangeSchedule():
	pairs = dt.PairsToday()

	global schedules
	schedules = []
	for i in pairs:
	 	job = schedule.every().day.at(cfg.schedule[i]).do(auth.StartLesson, fromSchedule = True).tag(str(i))
	 	schedules.append(job)

def DeleteAllSchedule():
	for i in schedules:
		schedule.cancel_job(i)

	schedules.clear()

def DeleteSchedule(i = 0):
	schedule.clear(str(i))
	schedules.pop(i)

def CheckSchedules():
	print(schedule.get_jobs())

def StartSchedule():
	if (dt.toNormalTime() > dt.toNormalTime('08:00:00')): 
		ChangeSchedule()
		schedule.every().day.at('08:00:00').do(ChangeSchedule).tag('0')
	else:
		schedule.every().day.at('08:00:00').do(ChangeSchedule).tag('0')
	schedule.every().day.at('23:59:00').do(DeleteAllSchedule).tag('64')
	CheckSchedules()	

	while True:
		schedule.run_pending()
		time.sleep(1)


if __name__ == '__main__':
	StartSchedule()
