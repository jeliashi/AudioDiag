#!/bin/python3

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
from PyQt5.QtCore import *



class LineNumberArea(QWidget):
	def __init__(self, editor):
		super().__init__()
		self.editor = editor

	def sizeHint(self):
		return QSize(self.editor.lineNumberAreaWidth(),0)

	def paintEvent(self, event):
		print('LineNumberArea.paintEvent')
		self.editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
	def __init__(self):
		super().__init__()
		self.lineNumberArea = LineNumberArea(self)

		self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
		self.updateRequest.connect(self.updateLineNumberArea)
		self.cursorPositionChanged.connect(self.highlightCurrentLine)

		self.updateLineNumberAreaWidth(0)

	def lineNumberAreaWidth(self):
		digits = 1
		count = max(1,self.blockCount())
		while count >= 10:
			count /= 10
			digits += 1
		space = 3 + self.fontMetrics().width('9')*digits
		return space

	def updateNumberAreaWidth(self):
		n_lines = self.blockCount()
		digits = np.ceil(np.log10(n_lines))
		self.lineNumberAreaWidth()
		return digits * QFontMetrics(self.font()).width('9') + 3

	def updateLineNumberAreaWidth(self, _):
		self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
		self.updateNumberAreaWidth()

	def updateLineNumberArea(self, rect, dy):
		if dy:
			self.lineNumberArea.scroll(0, dy)
		else:
			self.lineNumberArea.update(0,0, self.lineNumberArea.width(),
			                          rect.height())

		if rect.contains(self.viewport().rect()):
			self.updateLineNumberAreaWidth(0)


	def resizeEvent(self, event):
		super().resizeEvent(event)

		cr = self.contentsRect()
		self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
		                                      self.lineNumberAreaWidth(), cr.height()))

	def lineNumberAreaPaintEvent(self, event):
		painter = QPainter(self.lineNumberArea)
		print('CodeEditor.lineNumberAreaPaintEvent')
		painter.fillRect(event.rect(), Qt.lightGray)

		block = self.firstVisibleBlock()
		blockNumber = block.blockNumber()
		top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
		bottom = top + self.blockBoundingRect(block).height()

		height = self.fontMetrics().height()

		while block.isValid() and (top <= event.rect().bottom()):
			if block.isVisible() and (bottom >= event.rect().top()):
				number = str(blockNumber + 1)
				painter.setPen(Qt.darkBlue)
				painter.drawText(0, int(top), self.lineNumberArea.width(), height,
				                 Qt.AlignRight, number)

			block = block.next()
			top = bottom
			bottom = top + self.blockBoundingRect(block).height()
			blockNumber += 1

	def highlightCurrentLine(self):
		extraSelections = []

		if not self.isReadOnly():
			selection = QTextEdit.ExtraSelection()

			lineColor = QColor(Qt.yellow).lighter(160)

			selection.format.setBackground(lineColor)
			selection.format.setProperty(QTextFormat.FullWidthSelection, True)
			selection.cursor = self.textCursor()
			selection.cursor.clearSelection()
			extraSelections.append(selection)
		self.setExtraSelections(extraSelections)


class NCL_Editor(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)
		self.createEditor()

	def createEditor(self):
		self.tab_bar = QTabBar(movable=True, tabsClosable=True)
		self.tab_bar.tabCloseRequested.connect(self.CloseTab)
		self.tab_bar.tabBarClicked.connect(self.SwitchTab)

		self.tab_bar.setCurrentIndex(0)
		self.tab_bar.setLayoutDirection(Qt.LeftToRight)
		self.tab_bar.setElideMode(Qt.ElideLeft)

		self.tabCount = 0
		self.activeTabs = 0
		self.tabs = []
		self.container = QWidget()
		self.container.layout = QStackedLayout()
		self.container.setLayout(self.container.layout)

		self.AddNewTab()

		self.layout.addWidget(self.tab_bar)
		self.layout.addWidget(self.container)

	def CloseTab(self,i):
		self.tab_bar.removeTab(i)
		self.activeTabs -= 1
		if self.activeTabs == 0:
			self.AddNewTab()
			self.activeTabs += 1
		print(self.tabs)
		# self.tabCount -= 1

	def SwitchTab(self,i):
		if self.tab_bar.tabData(i):
			tab_data = self.tab_bar.tabData(i)["object"]

			tab_widget = self.findChild(QWidget, tab_data)
			self.container.layout.setCurrentWidget(tab_widget)

	def AddNewTab(self):
		i = self.tabCount

		self.activeTabs += 1
		self.tabs.append(QWidget())
		self.tabs[i].layout = QVBoxLayout()
		self.tabs[i].layout.setContentsMargins(0, 0, 0, 0)
		self.tabs[i].setObjectName("Tab"+str(i))

		self.tabs[i].content = CodeEditor()

		self.tabs[i].layout.addWidget(self.tabs[i].content)
		self.tabs[i].setLayout(self.tabs[i].layout)
		self.container.layout.addWidget(self.tabs[i])
		self.container.layout.setCurrentWidget(self.tabs[i])

		self.tab_bar.addTab("unnamed")
		self.tab_bar.setTabData(i,{"object":"unamed"+str(i)})
		self.tab_bar.setCurrentIndex(i)

		self.tabCount += 1


	def AddTab(self, file_string):
		i = self.tabCount
		self.activeTabs += 1

		self.tabs.append(QWidget())
		self.tabs[i].layout = QVBoxLayout()
		self.tabs[i].layout.setContentsMargins(0,0,0,0)
		self.tabs[i].setObjectName(file_string.rsplit('/',1)[1])
		self.tabs[i].content = CodeEditor()

		file = QFile(file_string)
		file.open(QFile.ReadOnly)
		self.tabs[i].content.setPlainText(QTextStream(file).readAll())

		self.tabs[i].layout.addWidget(self.tabs[i].content)

		self.tabs[i].setLayout(self.tabs[i].layout)
		self.container.layout.addWidget(self.tabs[i])
		self.container.layout.setCurrentWidget(self.tabs[i])

		self.tab_bar.addTab(file_string.rsplit('/',1)[1])
		self.tab_bar.setTabData(i,{"object":file_string.rsplit('/',1)[1]})
		self.tab_bar.setCurrentIndex(i)

		self.tabCount += 1


class NCL_Toolbar(QWidget):
	def __init__(self, editor):
		super().__init__()
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.editor = editor
		self.CreateToolBar()

	def CreateToolBar(self):
		self.new_script = QPushButton()
		self.new_script.pix_map = QPixmap('icons/new_script.png')
		self.new_script.setIcon(QIcon(self.new_script.pix_map))
		self.new_script.setIconSize(self.new_script.pix_map.rect().size())
		self.layout.addWidget(self.new_script)
		self.new_script.clicked.connect(self.editor.AddNewTab)

		self.open_file = QPushButton()
		self.open_file.pix_map = QPixmap('icons/open.png')
		self.open_file.setIcon(QIcon(self.open_file.pix_map))
		self.open_file.setIconSize(self.open_file.pix_map.rect().size())
		self.layout.addWidget(self.open_file)

		self.save_script = QPushButton()
		self.save_script.pix_map = QPixmap('icons/save.png')
		self.save_script.setIcon(QIcon(self.save_script.pix_map))
		self.save_script.setIconSize(self.save_script.pix_map.rect().size())
		self.layout.addWidget(self.save_script)

		self.saveas = QPushButton()
		self.saveas.pix_map = QPixmap('icons/saveAs.png')
		self.saveas.setIcon(QIcon(self.saveas.pix_map))
		self.saveas.setIconSize(self.saveas.pix_map.rect().size())
		self.layout.addWidget(self.saveas)

		self.run_script = QPushButton()
		self.run_script.pix_map = QPixmap('icons/run.png')
		self.run_script.setIcon(QIcon(self.run_script.pix_map))
		self.run_script.setIconSize(self.run_script.pix_map.rect().size())
		self.layout.addWidget(self.run_script)

		self.restart_session = QPushButton()
		self.restart_session.pix_map = QPixmap('icons/restart.png')
		self.restart_session.setIcon(QIcon(self.restart_session.pix_map))
		self.restart_session.setIconSize(self.restart_session.pix_map.rect().size())
		self.layout.addWidget(self.restart_session)

		self.clear_session = QPushButton()
		self.clear_session.pix_map = QPixmap('icons/clear.png')
		self.clear_session.setIcon(QIcon(self.clear_session.pix_map))
		self.clear_session.setIconSize(self.clear_session.pix_map.rect().size())
		self.layout.addWidget(self.clear_session)

		self.quit_app = QPushButton()
		self.quit_app.pix_map = QPixmap('icons/quit.png')
		self.quit_app.setIcon(QIcon(self.quit_app.pix_map))
		self.quit_app.setIconSize(self.quit_app.pix_map.rect().size())
		self.layout.addWidget(self.quit_app)
		self.quit_app.clicked.connect(QCoreApplication.instance().quit)


class FolderContents(QWidget):
	def __init__(self, editor):
		super().__init__(editor)
		self.editor = editor
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.tView = QTreeView()
		self.createFileExplorer()

	def createFileExplorer(self):
		self.dirModel = QFileSystemModel()
		# self.fileModel = QFileSystemModel()
		# self.fmDialog = QDialog()

		# self.dirModel.setFilter()
		self.root = self.dirModel.setRootPath(QDir.homePath())
		self.dirModel.setFilter(QDir.NoDot | QDir.AllEntries)
		# self.dirModel.setFilter(QDir.AllDirs)
		self.tView.setModel(self.dirModel)
		self.layout.addWidget(self.tView)
		self.tView.setRootIndex(self.root)
		self.tView.doubleClicked.connect(self.clickAction)
		self.subdirs = 0
		self.current_dir = QDir.homePath()

	def clickAction(self, index):
		if index.data() == '..':
			if self.subdirs > 0:
					self.current_dir = self.current_dir.rsplit('/', 1)[0]
					self.tView.setRootIndex(self.dirModel.setRootPath(self.current_dir))
					self.subdirs -= 1
			# print(QDir(index.parent()).absoluteFilePath())
			# self.dirModel.setRootPath(QDir(index.parent()).absolutePath())
		elif self.dirModel.fileInfo(index).isDir():
			self.subdirs += 1
			self.current_dir = self.current_dir+'/'+str(index.data())
			self.tView.setRootIndex(index)
		elif self.dirModel.fileInfo(index).isFile():
			extension = index.data().rsplit('.',1)[1]
			if extension == 'nc' or extension == 'nc4':
				subprocess.call('ncview '+ self.current_dir+'/'+index.data(), shell=True)
			elif extension == 'ncl':
				self.editor.AddTab(self.current_dir+'/'+index.data())


class NCL_CommandLine(QWidget):
	def __init__(self):
		super().__init__()
		# self.wid = int(self.winId())

		### have to embed a qwindow, and then start a qprocess
		### with xterm -into winID and then start ncl in that embedded
		### xterm....

	#
	# def _start_process(self,prop, xargs):
	# 	child = QProcess()
	# 	self._processes.append(child)
	# 	child.start(prop, xargs)


class App(QFrame):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("NCL IDE")
		self.setMinimumSize(683, 384)
		self.setBaseSize(840, 473)
		self.CreateApp()

	def CreateApp(self):
		self.super_layout = QVBoxLayout()
		self.super_layout.setSpacing(0)
		self.setContentsMargins(0, 0, 0, 0)

		self.editor = NCL_Editor()

		self.tool_bar = NCL_Toolbar(self.editor)
		self.super_layout.addWidget(self.tool_bar)
		self.sub_layout_1 = QHBoxLayout()
		self.sub_layout_1.addWidget(FolderContents(self.editor))

		self.sub_layout_2 = QVBoxLayout()

		self.sub_layout_2.addWidget(self.editor)
		self.cmdline = NCL_CommandLine()
		self.sub_layout_2.addWidget(self.cmdline)

		self.sub_layout_1.addLayout(self.sub_layout_2)
		self.super_layout.addLayout(self.sub_layout_1)

		# self.container = QWidget()
		# self.container.layout = QStackedLayout()
		# self.container.setLayout(self.container.layout)
		self.setLayout(self.super_layout)
		self.show()
		# while self.cmdline.serial.waitForReadyRead():
		# 	print(self.cmdline.serial.readAll())




if __name__ == "__main__":
	app = QApplication(sys.argv)
	QApplication.setStyle('Windows')
	window = App()
	sys.exit(app.exec_())
