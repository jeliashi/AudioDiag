import pyaudio
import numpy as np
import threading
import atexit
from numpy import fromstring

class InputSound(object):
	def __init__(self, settings):
		self.in_port = settings.in_port
		self.samp_freq = settings.samp_freq
		self.CHUNK = int(self.samp_freq/20)

		self.p = pyaudio.PyAudio()


	def startIn(self):
		self.stream = self.p.open(format=pyaudio.paInt16,
		                          channels=1, rate=self.samp_freq,
		                          input=True,input_device_index=self.in_port,
		                          frames_per_buffer=int(self.samp_freq/20))
		# self.lock = threading.Lock()
		self.stop = False
		self.frames = []
		print('Connected to Mic')

	def stopIn(self):
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()

	# def new_frame(self, data, frame_count, time_info, status):
	# 	data = fromstring(data, 'int16')
	# 	with self.lock:
	# 		self.frames.append(data)
	# 		if self.stop:
	# 			return None, pyaudio.paComplete
	# 	return None, pyaudio.paContinue

	def get_frames(self):
		data = self.stream.read(int(self.samp_freq/20), exception_on_overflow=False)
		data = np.fromstring(data,'Int16')
		return data
		# with self.lock:
		# 	frames = self.frames
		# 	self.frames = []
		# 	return frames

class RefSound(object):
	def __init__(self, ref_port, samp_freq=48000):
		self.ref_port = ref_port
		self.samp_freq = samp_freq
		self.CHUNK = int(self.samp_freq/20)

		self.p = pyaudio.PyAudio()


	def startRef(self):
		self.stream = self.p.open(format=pyaudio.paFloat32, channels=1,
		                     rate=self.samp_freq, input=True,input_device_index=self.ref_port)




