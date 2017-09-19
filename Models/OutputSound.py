import pyaudio
from numpy import empty,nan,random, sin, pi, arange, float32
from pandas import DataFrame
import numpy as np
# import socket
# from time import sleep
# import threading


class OutputSound(object):
	def __init__(self, settings):
		self.settings = settings
		# self.out_port = settings.out_port
		# self.samp_freq = settings.samp_freq
		# self.generateBool = settings.generateBool
		# self.type = settings.type
		# self.subType = settings.subType
		# self.toneF = settings.toneF


		#produces signal in 0.1 second intervals
		self.CHUNK = int(self.settings.samp_freq)
		self.phase = 0

		self.p = pyaudio.PyAudio()

	def newValues(self, settings):
		self.settings = settings

	def startSound(self):
		self.stream = self.p.open(format=pyaudio.paFloat32, channels=1,
		                rate=self.settings.samp_freq,output=True,output_device_index=self.settings.out_port)

	def produceSound(self):
		out_data = float
		if self.settings.type == 'Noise':
			if self.settings.subType == 'Pink':
				out_data = self.PinkNoise(self.CHUNK, 16)
			else:
				out_data = np.empty(self.CHUNK)
		elif self.settings.type == 'Tone':
			if self.settings.subType == "Sine":
				out_data = self.SineWave(self.CHUNK, self.settings.toneF)
			else: out_data = np.empty(self.CHUNK)


		self.stream.write(out_data)

	def stopSound(self):
		self.stream.stop_stream()
		self.stream.close()


	def PinkNoise(self, nrows, ncols=16):
		array = empty((nrows, ncols))
		array.fill(nan)
		array[0, :] = random.random(ncols)
		array[:, 0] = random.random(nrows)

		cols = random.geometric(0.5, nrows)
		cols[cols >= ncols] = 0
		rows = random.randint(nrows, size=nrows)
		array[rows, cols] = random.random(nrows)

		df = DataFrame(array)
		df.fillna(method='ffill', axis=0, inplace=True)
		total = df.sum(axis=1)
		return total.values

	def WhiteNoise(self, nrows):
		pass

	def BlueNoise(self, nrows):
		pass

	def RedNoise(self, nrows):
		pass

	def SineWave(self, nrows, toneF):
		vals = 2*pi*arange(nrows)*(toneF)/nrows + self.phase
		samples = (sin(vals)).astype(float32)
		self.phase = 2*pi - vals[-1]%(2*pi)
		print(self.phase)
		return samples


	def TriWave(self, nrows, toneF):
		pass

	def SqWave(self, nrows, toneF):
		pass