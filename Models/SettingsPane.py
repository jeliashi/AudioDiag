import pyaudio
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QHBoxLayout, QRadioButton,
                             QWidget, QComboBox, QSpinBox, QCheckBox,
                             QGroupBox, QSlider, QPushButton)
from PyQt5.QtCore import Qt


class Settings:
	def __init__(self):
		self.generateBool = False
		self.type = 'Noise'
		self.subType = 'Pink'
		self.tone = 440
		self.out_port = 0
		self.in_port = 1
		self.ref_port = 1
		self.minF = 100
		self.maxF = 12000
		self.samp_freq = 48000


class SettingsPane(QWidget):
	def __init__(self):
		super().__init__()
		self.toneF = 440
		self.inputOptions = {}
		self.outputOptions = {}
		self.settings = Settings()
		p = pyaudio.PyAudio()
		info = p.get_host_api_info_by_index(0)
		N_dev = info.get('deviceCount')
		for i in range(0, N_dev):
			if p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
				self.inputOptions[p.get_device_info_by_host_api_device_index(0, i).get('name')] = i
			if p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels') > 0:
				self.outputOptions[p.get_device_info_by_host_api_device_index(0, i).get('name')] = i

		self.createUI()

	def createUI(self):
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		self.produceLayout = QVBoxLayout()

		self.produceBoolCheck = QCheckBox('Produce Sound:  ')
		self.produceBoolCheck.setChecked(False)
		self.produceType = QGroupBox()
		self.produceTone = QRadioButton('Tone')
		self.produceNoise = QRadioButton('Noise')
		self.produceToneBox = QGroupBox()
		self.produceSineTone = QRadioButton('Sine Wave')
		self.produceTriTone = QRadioButton('Triangle Wave')
		self.produceSqTone = QRadioButton('Square Wave')
		self.ToneSlider = QSlider(Qt.Horizontal)
		self.ToneSlider.setRange(20, 20000)
		self.ToneSlider.valueChanged.connect(self.newTone)
		self.ToneSlider.sliderReleased.connect(self.newTone)
		self.produceNoiseBox = QGroupBox()
		self.WhiteNoise = QRadioButton('White')
		self.PinkNoise = QRadioButton('Pink')
		self.RedNoise = QRadioButton('Red')
		self.BlueNoise = QRadioButton('Blue')

		self.toneBox = QVBoxLayout()
		self.toneBoxupper = QVBoxLayout()
		self.toneBoxupper.addWidget(self.produceSineTone)
		self.toneBoxupper.addWidget(self.produceTriTone)
		self.toneBoxupper.addWidget(self.produceSqTone)
		self.toneBox.addWidget(self.produceToneBox)
		self.toneBox.addWidget(self.ToneSlider)
		self.produceToneBox.setLayout(self.toneBoxupper)

		self.noiseBox = QVBoxLayout()
		self.noiseBox.addWidget(self.WhiteNoise)
		self.noiseBox.addWidget(self.PinkNoise)
		self.noiseBox.addWidget(self.RedNoise)
		self.noiseBox.addWidget(self.BlueNoise)
		self.produceNoiseBox.setLayout(self.noiseBox)

		self.produceBox = QVBoxLayout()
		self.produceBox.addWidget(self.produceTone)
		self.produceBox.addLayout(self.toneBox)
		self.produceBox.addWidget(self.produceNoise)
		self.produceBox.addWidget(self.produceNoiseBox)

		self.outlayout = QHBoxLayout()
		self.outLabel = QLabel('Output Device: ')
		self.outPortList = QComboBox()
		for key in self.outputOptions.keys():
			self.outPortList.addItem(key)

		self.outPortList.activated[str].connect(self.outActivate)
		self.outlayout.addWidget(self.outLabel)
		self.outlayout.addWidget(self.outPortList)

		self.inlayout = QHBoxLayout()
		self.inLabel = QLabel()
		self.inLabel.setText('Input Device:  ')
		self.inPortList = QComboBox()
		for key in self.inputOptions.keys():
			self.inPortList.addItem(key)

		self.inPortList.activated[str].connect(self.inActivate)
		self.inlayout.addWidget(self.inLabel)
		self.inlayout.addWidget(self.inPortList)

		self.reflayout = QHBoxLayout()
		self.refLabel = QLabel()
		self.refLabel.setText('Reference Device:  ')
		self.refPortList = QComboBox()
		for key in self.inputOptions.keys():
			self.refPortList.addItem(key)

		self.refPortList.activated[str].connect(self.refActivate)
		self.reflayout.addWidget(self.refLabel)
		self.reflayout.addWidget(self.refPortList)

		self.lowFreqlayout = QHBoxLayout()
		self.lowFreqLabel = QLabel()
		self.lowFreqLabel.setText('Lower Freq Limit (Hz)')
		self.lowFreqSlider = QSpinBox()
		self.lowFreqSlider.setRange(20, 1000)
		self.lowFreqSlider.setValue(100)
		self.lowFreqSlider.valueChanged.connect(self.lowFChange)
		self.lowFreqlayout.addWidget(self.lowFreqLabel)
		self.lowFreqlayout.addWidget(self.lowFreqSlider)

		self.highFreqlayout = QHBoxLayout()
		self.highFreqLabel = QLabel()
		self.highFreqLabel.setText('Upper Freq Limit (Hz)')
		self.highFreqSlider = QSpinBox()
		self.highFreqSlider.setRange(5000, 20000)
		self.highFreqSlider.setValue(12000)
		self.highFreqSlider.valueChanged.connect(self.highFChange)
		self.highFreqlayout.addWidget(self.highFreqLabel)
		self.highFreqlayout.addWidget(self.highFreqSlider)

		self.updateSettingsButton = QPushButton('Update Settings')
		self.updateSettingsButton.pressed.connect(self.updateSettings)

		self.layout.addLayout(self.produceBox)

		self.layout.addLayout(self.outlayout)
		self.layout.addLayout(self.inlayout)
		self.layout.addLayout(self.reflayout)
		self.layout.addLayout(self.lowFreqlayout)
		self.layout.addLayout(self.highFreqlayout)
		self.layout.addWidget(self.updateSettingsButton)

	def outActivate(self, key):
		self.settings.out_port = self.outputOptions[key]

	def inActivate(self, key):
		self.settings.in_port = self.inputOptions[key]

	def refActivate(self, key):
		self.settings.ref_port = self.inputOptions[key]

	def lowFChange(self):
		self.settings.minF = self.lowFreqSlider.value()

	def highFChange(self):
		self.settings.maxF = self.highFreqSlider.value()

	def newTone(self):
		self.toneF = self.ToneSlider.value()

	def updateSettings(self):
		self.settings.generateBool = self.produceBoolCheck.isChecked()
		if self.produceTone.isChecked():
			self.settings.type = 'tone'
			if self.produceSineTone.isChecked():
				self.settings.subType = 'Sine'
			elif self.produceTriTone.isChecked():
				self.settings.subType = 'Triangle'
			else:
				self.settings.subType = 'Square'
			self.settings.tone = self.toneF
		else:
			self.settings.type = 'Noise'
			if self.WhiteNoise.isChecked():
				self.settings.subType = 'White'
			elif self.PinkNoise.isChecked():
				self.settings.subType = 'Pink'
			elif self.RedNoise.isChecked():
				self.settings.subType = 'Red'
			else:
				self.settings.subType = 'Blue'
