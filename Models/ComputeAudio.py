from PyQt5.QtWidgets import QWidget
from .InputSound import *
from .OutputSound import *
from PyQt5.QtCore import pyqtSlot, QRunnable, QThreadPool
import time


class Graphs(QRunnable):
	'''
	Thread for the graphs
	'''
	def __init__(self, settings):
		super(Graphs, self).__init__()
		self.settings = settings
		self.settings.changedValue.connect(self.adjustParams)

	@pyqtSlot()
	def run(self):
		'''
		Code to run
		'''
		while True:
			print("graphs Started")
			time.sleep(7)

	def adjustParams(self, val):
		print(val)


class Sounds(QRunnable):
	'''
	:param args: Arguments to make available to run code
	:param kwargs: Keyword arguments to make available to run code
	'''
	def __init__(self, settings, *args, **kwargs):
		super(Sounds, self).__init__()
		self.args = args
		self.kwargs = kwargs
		self.settings = settings
		self.outStream = OutputSound(self.settings)
		self.outStream.startSound()

	@pyqtSlot()
	def run(self):
		'''
		Sounds to run
		'''
		self.outStream = OutputSound(self.settings)
		self.outStream.startSound()
		while True:

			if self.settings.generateBool== True:
				self.outStream.newValues(self.settings)
				self.outStream.produceSound()
			if self.settings.toneF == -1:
				break


	# def adjustParams(self, val):
	# 	self.outStream.newValues(self.settings)


class AudioDisplay(QWidget):
	def __init__(self, settings):
		super().__init__()
		self.threadPool = QThreadPool()
		# self.settings.
		self.graphs = Graphs(settings)
		self.threadPool.start(self.graphs)
		self.sounds = Sounds(settings)
		self.threadPool.start(self.sounds)



