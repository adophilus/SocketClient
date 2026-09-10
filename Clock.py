from time import sleep
from threading import Thread
from datetime import datetime

class Clock(object):
	def __init__(self):
		self.ctime = 0
		self.isTicking = False
		self.timeThread = Thread(target = self.tick)

	def start(self):
		if not self.isTicking:
			self.timeThread.start()

	def tick(self):
		while self.isTicking:
			self.ctime += .5
			sleep(.5)

	def stop(self):
		self.isTicking = False

	def wait(self, time):
		sleep(time)
	
	def date(self):
		return str(datetime.now().strftime('%Y-%m-%d'))

	def time(self):
		return str(datetime.now().strftime('%H:%M:%S'))

	def get(self):
		return int(self.ctime)

if __name__ == '__main__':
	h = Clock()
	h.start()
	sleep(3)
	h.stop()
	while True:
		t = h.get()
		print(t)
		sleep(3)