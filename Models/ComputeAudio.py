from PyQt5.QtWidgets import QWidget
from .InputSound import *
from .OutputSound import *

class AudioDisplay(QWidget):
	def __init__(self, settings):
		super().__init__()
		self.out_port = settings.out_port
		self.in_port = settings.in_port
		self.ref_port = settings.ref_port
		self.minF = settings.minF
		self.maxF = settings.maxF
		self.samp_freq = settings.samp_freq

