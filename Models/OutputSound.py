from .Noise import Noise
import pyaudio
import numpy as np
import socket
from time import sleep
import threading


class OutputSound(object):
	def __init__(self, out_port, samp_freq=48000, generateBool=True,
	             type='Noise', subType='Pink'):
		self.out_port = out_port
		self.samp_freq = samp_freq
		self.generateBool = generateBool
		self.type = type
		self.subType = subType


		#produces signal in 0.1 second intervals
		self.CHUNK = int(self.samp_freq/10)

		p = pyaudio.PyAudio()

		self.stream = p.open(format=pyaudio.paFloat32, channels=1,
		                rate=self.samp_freq,output=True,output_device_index=self.out_port)

		self.outProducer = Noise(generate=True,samp_freq=self.samp_freq)


	def produceSound(self):
		if self.generateBool == True:

			if self.type == 'Noise':
				if self.subType == 'Pink':
					out_data = self.outProducer.PinkNoise(self.CHUNK, 16)
				else:
					out_data = np.empty(self.CHUNK)


			self.stream.write(out_data)

	def stopSound(self):
		self.stream.stop_stream()
		self.stream.close()



