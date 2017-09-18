import sys
import os
import json
import numpy as np
import subprocess

import atexit

from PyQt5.QtSerialPort import *

from PyQt5.QtWidgets import (QTextEdit, QFrame, QVBoxLayout,
                             QHBoxLayout, QTabBar, QWidget,
                             QApplication, QStackedLayout,
                             QPushButton, QShortcut, QSplitter,
                             QStyleFactory, QFileSystemModel, QDialog,
                             QTreeView, QPlainTextEdit)
from PyQt5.QtGui import *

class SettingsPane(QWidget):
	def __init__(self, global_settings):
		super().__init__()
		self.settings = global_settings
		