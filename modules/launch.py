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
	for i in pairs:
	 	schedule.every().day.at(cfg.schedule[i]).do(auth.StartLesson, fromSchedule = True)


def main():
	# for i in cfg.schedule:
	# 	schedule.every().day.at(i).do(auth.StartLesson)

	schedule.every().day.at('00:00').do(ChangeSchedule)

	while True:
		schedule.run_pending()
		time.sleep(1)


if __name__ == '__main__':
	main()
