# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'css_editor\untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import PyQt4
# from PyQt4 import *
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4 import QtNetwork
import time
import syntax
import os
import os.path
from bs4 import BeautifulSoup

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)
		
class WebView(QtWebKit.QWebView):

	def __init__(self, parent=None):
		QtWebKit.QWebView.__init__(self, parent)

	def contextMenuEvent(self, event):
		# override this method and do nothing.
		pass
		

class Ui_Dialog(object):
	def setupUi(self, Dialog):
		self.dialog = Dialog
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(1024, 768)
		Dialog.setMinimumSize(QtCore.QSize(1024, 768))
		Dialog.setStyleSheet(_fromUtf8("background-color: rgb(150, 150, 150);"))
		self.horizontalLayout_6 = QtGui.QHBoxLayout(Dialog)
		self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		self.verticalLayout_2.setSpacing(0)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.horizontalLayout_4 = QtGui.QHBoxLayout()
		self.horizontalLayout_4.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
		self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		self.radioButton_contentTable = QtGui.QRadioButton(Dialog)
		self.radioButton_contentTable.setMinimumSize(QtCore.QSize(120, 30))
		self.radioButton_contentTable.setMaximumSize(QtCore.QSize(120, 30))
		self.radioButton_contentTable.setStyleSheet(_fromUtf8("background-color: rgb(204, 204, 204);\n"
"padding-left:5px;"))
		self.radioButton_contentTable.setChecked(True)
		self.radioButton_contentTable.setObjectName(_fromUtf8("radioButton_contentTable"))
		self.radioButton_contentTable.clicked.connect(self.changePage)#signal
		self.horizontalLayout_4.addWidget(self.radioButton_contentTable)
		spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacerItem)
		self.radioButton_chapter1 = QtGui.QRadioButton(Dialog)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.radioButton_chapter1.sizePolicy().hasHeightForWidth())
		self.radioButton_chapter1.setSizePolicy(sizePolicy)
		self.radioButton_chapter1.setMinimumSize(QtCore.QSize(120, 30))
		self.radioButton_chapter1.setMaximumSize(QtCore.QSize(120, 30))
		self.radioButton_chapter1.setStyleSheet(_fromUtf8("background-color: rgb(204, 204, 204);padding-left:5px;"))
		self.radioButton_chapter1.setObjectName(_fromUtf8("radioButton_chapter1"))
		self.radioButton_chapter1.clicked.connect(self.changePage)#signal
		self.horizontalLayout_4.addWidget(self.radioButton_chapter1)
		spacerItem1 = QtGui.QSpacerItem(320, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacerItem1)
		self.verticalLayout_2.addLayout(self.horizontalLayout_4)
		self.horizontalLayout_5 = QtGui.QHBoxLayout()
		self.horizontalLayout_5.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
		self.webView = WebView(Dialog)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
		self.webView.setSizePolicy(sizePolicy)
		self.webView.setMinimumSize(QtCore.QSize(400, 720))
		self.webView.setMaximumSize(QtCore.QSize(500, 16777215))
		self.webView.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
		self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
		self.webView.setObjectName(_fromUtf8("webView"))
		self.horizontalLayout_5.addWidget(self.webView)
		self.verticalLayout_2.addLayout(self.horizontalLayout_5)
		self.horizontalLayout.addLayout(self.verticalLayout_2)
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout_4 = QtGui.QVBoxLayout()
		self.verticalLayout_4.setSpacing(0)
		self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
		self.horizontalLayout_8 = QtGui.QHBoxLayout()
		self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
		spacerItem2 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		self.horizontalLayout_8.addItem(spacerItem2)
		self.verticalLayout_4.addLayout(self.horizontalLayout_8)
		self.horizontalLayout_9 = QtGui.QHBoxLayout()
		self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
		self.plainTextEdit = QtGui.QPlainTextEdit(Dialog)
		self.plainTextEdit.setMinimumSize(QtCore.QSize(300, 720))
		self.plainTextEdit.setAcceptDrops(False)
		self.plainTextEdit.setReadOnly(True)
		self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
		self.plainTextEdit.setStyleSheet(_fromUtf8("background-color: rgb(220, 220, 220);"))
		self.horizontalLayout_9.addWidget(self.plainTextEdit)
		self.verticalLayout_4.addLayout(self.horizontalLayout_9)
		self.horizontalLayout.addLayout(self.verticalLayout_4)
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.label = QtGui.QLabel(Dialog)
		self.label.setMinimumSize(QtCore.QSize(80, 30))
		self.label.setMaximumSize(QtCore.QSize(80, 30))
		self.label.setAutoFillBackground(False)
		self.label.setStyleSheet(_fromUtf8("background-color: rgb(117, 117, 117);\n"
"color: rgb(255, 255, 255);\n"
"padding-left:6px;"))
		self.label.setObjectName(_fromUtf8("label"))
		self.horizontalLayout_2.addWidget(self.label)
		spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem2)
		self.pushButtonPreview = QtGui.QPushButton(Dialog)
		self.pushButtonPreview.setMinimumSize(QtCore.QSize(0, 30))
		self.pushButtonPreview.setObjectName(_fromUtf8("pushButtonPreview"))
		self.pushButtonPreview.clicked.connect(self.clickPreview)#signal
		self.horizontalLayout_2.addWidget(self.pushButtonPreview)
		self.pushButtonSave = QtGui.QPushButton(Dialog)
		self.pushButtonSave.setMinimumSize(QtCore.QSize(0, 30))
		self.pushButtonSave.setObjectName(_fromUtf8("pushButtonSave"))
		self.pushButtonSave.clicked.connect(self.clickSave)#signal
		self.horizontalLayout_2.addWidget(self.pushButtonSave)
		self.verticalLayout.addLayout(self.horizontalLayout_2)
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		self.textEdit = QtGui.QPlainTextEdit(Dialog)
		self.textEdit.setStyleSheet(_fromUtf8("background-color: rgb(220, 220, 220);"))
		self.textEdit.setObjectName(_fromUtf8("textEdit"))
		self.textEdit.setMinimumSize(QtCore.QSize(0, 720))
		self.horizontalLayout_3.addWidget(self.textEdit)
		self.verticalLayout.addLayout(self.horizontalLayout_3)
		self.horizontalLayout.addLayout(self.verticalLayout)
		self.horizontalLayout_6.addLayout(self.horizontalLayout)

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Style Editor", None))
		self.radioButton_contentTable.setText(_translate("Dialog", "Content Table", None))
		self.radioButton_chapter1.setText(_translate("Dialog", "Chapter1", None))
		self.label.setText(_translate("Dialog", "CSS Style", None))
		self.pushButtonPreview.setText(_translate("Dialog", "<= Preview", None))
		self.pushButtonPreview.setStyleSheet(_fromUtf8("background-color: rgb(220, 220, 220);"))
		self.pushButtonSave.setText(_translate("Dialog", "> Save <", None))
		self.pushButtonSave.setStyleSheet(_fromUtf8("background-color: rgb(220, 220, 220);"))

	def main(self):
		file1  = open("./ressources/loading_fonts.txt", "r")
		file2  = open("./ressources/common.css", "r")
		self.current_style_font = file1.read()
		css = file2.read()
		file1.close()
		file2.close()
		self.highlight = syntax.PythonHighlighter(self.textEdit.document())
		self.textEdit.setPlainText(css)
		self.highlight.rehighlight()
		
		self.highlightTimer = PyQt4.QtCore.QTimer()
		self.highlightTimer.timeout.connect(self.redoTextHighlight)
		self.highlightTimer.start(200)
		
		self.checkFontLastTime = float(os.path.getmtime("./ressources/loading_fonts.txt"))
		self.checkFontTimer = PyQt4.QtCore.QTimer()
		self.checkFontTimer.timeout.connect(self.updateFont)
		self.checkFontTimer.start(200)
		self.changePage()
		
		self.dialog.show()
	
	def updateFont(self):
		newTime = float(os.path.getmtime("./ressources/loading_fonts.txt"))
		if self.checkFontLastTime < newTime:
			self.checkFontLastTime = newTime
			file1  = open("./ressources/loading_fonts.txt", "r")
			self.current_style_font = file1.read()
			file1.close()
			self.clickPreview()
	
	def redoTextHighlight(self):
		self.highlightTimer.start(200)
		self.highlight.rehighlight()
	
	def changePage(self):
		current_url = self.webView.url().toString()
		current_is_toc = False
		if 'toc.xhtml' in current_url:
			current_is_toc = True
		check_is_toc = self.radioButton_contentTable.isChecked()
		if check_is_toc is not current_is_toc:
			print('changePage')
			if check_is_toc is True:
				self.webView.setUrl(PyQt4.QtCore.QUrl(_fromUtf8("tmp/toc.xhtml")))
				file2  = open("./tmp/toc.xhtml", "rb")
				
			else:
				self.webView.setUrl(PyQt4.QtCore.QUrl(_fromUtf8("tmp/ch-1.xhtml")))
				file2  = open("./tmp/ch-1.xhtml", "rb")
			soup = BeautifulSoup(file2, 'html.parser')
			self.plainTextEdit.setPlainText(soup.prettify())
			file2.close()
				
	def clickPreview(self):
		text = self.textEdit.document().toPlainText()
		file3  = open("./tmp/common.css", "w")
		file3.write(text.replace('<FONT>', self.current_style_font))
		file3.close()
		self.webView.reload()
				
	def clickSave(self):
		text = self.textEdit.document().toPlainText()
		#print(text)
		print('Sauvegarde css')
		file3  = open("./ressources/common.css", "w")
		file3.write(text)
		file3.close()
		self.webView.reload()
		
