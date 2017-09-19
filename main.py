from Models.OutputSound import OutputSound
from Models.SettingsPane import SettingsPane
from Models.ComputeAudio import AudioDisplay

import sys

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class App(QFrame):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Audio Diagnostics")
		self.setMinimumSize(683,384)
		self.setBaseSize(840,473)
		self.CreateApp()

	def CreateApp(self):
		self.container = QHBoxLayout()
		self.container.setSpacing(0)
		self.setContentsMargins(0, 0, 0, 0)

		self.settings = SettingsPane()
		self.audioDisplay = AudioDisplay(self.settings.settings)

		self.container.addWidget(self.settings)
		self.setLayout(self.container)

		self.show()

if __name__ == "__main__":
	# x = OutputSound(1, generateBool=False)
	# while True:
	# 	for i in range(1000000):
	# 		x.generateBool = False
	# 		x.produceSound()
	# 	x.generateBool=True
	# 	x.produceSound()
	app = QApplication(sys.argv)
	QApplication.setStyle('Fusion')
	window = App()
	sys.exit(app.exec_())
