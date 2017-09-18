from matplotlib.backends.backend_qt5agg import FigureCanvasAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from scipy.signal import csd

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QCheckBox, QSlider)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui

import sys
import pyaudio
import wave

import numpy as np
import threading
import atexit

class MplFigure(object):
	def __init__(self, parent):
		self.figure = plt.figure(facecolor='white')
		self.canvas = Canvas(self.figure)
		self.toolbar = NavBar(self.canvas, parent)


class MicrophoneRecorder(object):
	def __init__(self, rate=4000, chunksize=1024):
		self.rate = rate
		self.ChunkSize = chunksize

		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format=pyaudio.paInt16,
		                          channels=1, rate=self.rate,
		                          input=True, frames_per_buffer=self.ChunkSize,
		                          stream_callback=self.new_frame)
		self.lock = threading.Lock()
		self.stop = False

		self.frames = []
		atexit.register(self.close)

		def new_frame(self, data, frame_count, time_info, status):
			data = np.fromstring(data, 'int16')
			with self.lock:
				self.frames.append(data)
				if self.stop:
					return None, pyaudio.paComplete
			return None, pyaudio.paContinue

		def get_frames(self):
			with self.lock:
				frames = self.frames
				self.frames = []
				return frames

		def start(self):
			self.stream.start_stream()

		def close(self):
			with self.lock:
				self.stop = True
			self.stream.close()
			self.p.terminate()

class LiveFFTWidget(QWidget):
	def __init__(self):
		super().__init__()

		self.initUI()
		self.initData()
		self.connectSlots()
		self.initMplWidget()

	def initUI(self):
		hbox_gain = QHBoxLayout()
		autoGain = QLabel('Auto gain for frequency spectrum')
		autoGainCheckBox = QCheckBox(checked=True)
		hbox_gain.addWidget(autoGain)
		hbox_gain.addWidget(autoGainCheckBox)

		self.autoGainCheckBox = autoGainCheckBox

		hbox_fixedGain = QHBoxLayout()
		fixedGain = QLabel('Manual gain level for frequency spectrum')
		fixedGainSlider = QSlider(QtCore.Qt.Horizontal)
		hbox_fixedGain.addWidget(fixedGain)
		hbox_fixedGain.addWidget(fixedGainSlider)

		self.fixedGainSlider = fixedGainSlider

		self.vbox = QVBoxLayout()

		self.vbox.addLaout(hbox_gain)
		self.vbox.addLayout(hbox_fixedGain)

		self.main_figure = MplFigure(self)
		self.vbox.addWidget(self.main_figure.toolbar)
		self.vbox.addWidget(self.main_figure.canvas)

		self.setLayout(self.vbox)

		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('LiveFFT')
		self.show()

		timer = QtCore.QTimer()
		timer.timeoutconnect(self.handleNewData)
		timer.start(100)
		self.timer = timer


	def initData(self):
		self.mic = MicrophoneRecorder()
		self.mic.start()

		self.freq_vect = np.fft.rfftfreq(self.mic.chunksize,1./self.mic.rate)
		self.time_vect = np.arrange(mic.chunksize, dtype=np.float32) / mic.rate * 1000

	def connectSlots(self):
		pass

	def initMplWidget(self):
		pass

	def handleNewData(self):
		pass
