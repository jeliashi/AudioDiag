import pyaudio

class InputSound(object):
	def __init__(self, in_port, samp_freq=48000):
		self.in_port = in_port
		self.samp_freq = samp_freq
		self.CHUNK = int(self.samp_freq/10)

		p = pyaudio.PyAudio()

		self.stream = p.open(format=pyaudio.paFloat32, channels=1,
		                     rate=self.samp_freq, input=True,input_device_index=self.in_port)

class RefSound(object):
	def __init__(self, ref_port, samp_freq=48000):
		self.ref_port = ref_port
		self.samp_freq = samp_freq
		self.CHUNK = int(self.samp_freq/10)

		p = pyaudio.PyAudio()

		self.stream = p.open(format=pyaudio.paFloat32, channels=1,
		                     rate=self.samp_freq, input=True,input_device_index=self.ref_port)

