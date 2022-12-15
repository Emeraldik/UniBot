import schedule
import authentification as auth
import time
import date as dt
import main_module as mm

import threading

import sys

sys.path.insert(0, '../cfg')

import config as cfg


def ChangeSchedule():
  pairs = dt.PairsToday()

  global schedules
  schedules = []
  for i in pairs:
    job = schedule.every().day.at(cfg.schedule[i]).do(auth.StartLesson, fromSchedule=True).tag(str(i))
    schedules.append(job)


def DeleteAllSchedule(stop=False):
  for i in schedules:
    schedule.cancel_job(i)

  if stop:
    schedule.clear('0')
  schedules.clear()
  #print(threading.current_thread())


def DeleteSchedule(i=0):
  schedule.clear(str(i))
  schedules.pop(i)


def CheckSchedules():
  print(schedule.get_jobs())


def StartSchedule():
	if (dt.toNormalTime() > dt.toNormalTime('05:00:00')):
		ChangeSchedule()
		schedule.every().day.at('05:00:00').do(ChangeSchedule).tag('0')
	else:
		schedule.every().day.at('05:00:00').do(ChangeSchedule).tag('0')

	schedule.every().day.at('20:59:00').do(DeleteAllSchedule).tag('64')

	while True:
		schedule.run_pending()
		time.sleep(1)

def StartSchedule_Mail():
	schedule.every(1).minutes.do(mm.checkBOTMail, message=cfg.chat_ID).tag('128')

	while True:
	    schedule.run_pending()
	    time.sleep(1)

if __name__ == '__main__':
  StartSchedule()
