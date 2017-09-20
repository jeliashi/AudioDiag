from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QCheckBox, QSlider)
from .InputSound import *
from .OutputSound import *
from PyQt5.QtCore import pyqtSlot, QRunnable, QThreadPool, Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import time
import numpy as np


class MplFigure(object):
	def __init__(self, parent):
		self.figure = plt.figure(facecolor='white')
		self.canvas = Figure(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, parent)

class Graphs(QRunnable):
	'''
	Thread for the graphs
	'''
	def __init__(self, settings, mpl_figure, auto_gain, gain_slide):
		super(Graphs, self).__init__()
		self.autoGainCheckBox = auto_gain
		self.fixedGainSlider = gain_slide
		self.settings = settings
		self.settings.changedValue.connect(self.adjustParams)
		# self.timer = QTimer()
		# self.timer.timeout.connect(self.handleNewData)
		# self.timer.start(10)

		self.mpl_figure = mpl_figure
		self.input = InputSound(settings)
		self.input.startIn()

		self.freq_vect = np.fft.rfftfreq(int(self.settings.samp_freq/20),
		                                 1./self.settings.samp_freq )
		print('length of freq vect: ', len(self.freq_vect))
		self.time_vect = np.arange(self.settings.samp_freq/20, dtype=np.float32)/self.settings.samp_freq*1000
		print('length of time vect: ', len(self.time_vect))

		self.ax_top = self.mpl_figure.figure.add_subplot(211)
		self.ax_top.set_ylim(-32768)
		self.ax_top.set_xlim(0, self.time_vect.max())
		self.ax_top.set_xlabel(u'time (ms)', fontsize=6)

		self.ax_bottom = self.mpl_figure.figure.add_subplot(212)
		self.ax_bottom.set_ylim(0, 1)
		self.ax_bottom.set_xlim(0, self.freq_vect.max())
		self.ax_bottom.set_xlabel(u'frequency (Hz)', fontsize=6)
		self.line_top, = self.ax_top.plot(self.time_vect,
		                                  np.ones_like(self.time_vect))

		self.line_bottom, = self.ax_bottom.plot(self.freq_vect,
		                                        np.ones_like(self.freq_vect))


	def handleNewData(self):
		data = self.input.get_frames()
		# current_frame = []
		if len(data) > 0:
			current_frame = data
			# Nt = len(self.time_vect)
			# if len(current_frame) > Nt:
			# 	current_frame = current_frame[-Nt:]
			self.line_top.set_data(self.time_vect[-len(current_frame):], current_frame)

			fft_frame = np.fft.rfft(current_frame)
			if self.autoGainCheckBox.isChecked() == True:
				fft_frame /= np.abs(fft_frame).max()
			else:
				fft_frame *= (1+ self.fixedGainSlider.value()) / 5000000.

			self.line_bottom.set_data(self.freq_vect[-len(fft_frame):], np.abs(fft_frame))

			self.mpl_figure.canvas.draw()


	def computeFFT(self):
		pass

	@pyqtSlot()
	def run(self):
		'''
		Code to run
		'''
		while True:
			self.handleNewData()

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

		self.sounds = Sounds(settings)
		self.threadPool.start(self.sounds)

		self.initUI()
		self.graphs = Graphs(settings, self.main_figure, self.autoGainCheckBox, self.fixedGainSlider)
		self.threadPool.start(self.graphs)

	def initUI(self):
		hbox_gain = QHBoxLayout()
		autoGain = QLabel('Auto gain for freq spectrum')
		self.autoGainCheckBox = QCheckBox(checked=True)
		hbox_gain.addWidget(autoGain)
		hbox_gain.addWidget(self.autoGainCheckBox)

		hbox_fixedGain = QHBoxLayout()
		fixedGain = QLabel('Manual gain level for frequency spectrum')
		self.fixedGainSlider = QSlider(Qt.Horizontal)
		hbox_fixedGain.addWidget(fixedGain)
		hbox_fixedGain.addWidget(self.fixedGainSlider)

		vbox = QVBoxLayout()
		vbox.addLayout(hbox_gain)
		vbox.addLayout(hbox_fixedGain)

		self.main_figure = MplFigure(self)
		vbox.addWidget(self.main_figure.toolbar)
		vbox.addWidget(self.main_figure.canvas)

		self.setLayout(vbox)
		# self.setGeometry(300,300,350,300)







