from PyQt4 import QtCore, QtGui
import sys
import os
import os.path
import ctypes
from bs4 import BeautifulSoup

import interface
import presetUI
import syntax

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

app = None
dialog = None
dialog2 = None
window2 = None
urlBase = 'file://'+os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/')
urlBase_clean = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/')
highlightTimer = None
highlight = None
checkFontTimer = None
checkFontLastTime = 0
current_style_font = ''


def updateFont():
	global dialog, urlBase_clean, checkFontLastTime, current_style_font
	newTime = float(os.path.getmtime(urlBase_clean+"/ressources/loading_fonts.txt"))
	if checkFontLastTime < newTime:
		checkFontLastTime = newTime
		file1 = open(urlBase_clean+"/ressources/loading_fonts.txt", "r")
		current_style_font = file1.read()
		file1.close()
		clickPreview()


def redoTextHighlight():
	global dialog, highlight
	highlight.rehighlight()


def changePage():
	global dialog, urlBase, urlBase_clean
	current_url = dialog.webView.url().toString()
	current_is_toc = False
	if 'toc.xhtml' in current_url:
		current_is_toc = True
	check_is_toc = dialog.radioButton_contentTable.isChecked()
	if check_is_toc is not current_is_toc:
		print('changePage')
		if check_is_toc is True:
			dialog.webView.setUrl(QtCore.QUrl(_fromUtf8(urlBase_clean+"/tmp/toc.xhtml")))
			file2 = open(urlBase_clean+"/tmp/toc.xhtml", "rb")
			
		else:
			dialog.webView.setUrl(QtCore.QUrl(_fromUtf8(urlBase_clean+"/tmp/ch-1.xhtml")))
			file2 = open(urlBase_clean+"/tmp/ch-1.xhtml", "rb")
		soup = BeautifulSoup(file2, 'html.parser')
		dialog.plainTextEdit.setPlainText(soup.prettify())
		file2.close()


def clickPreview():
	global dialog, urlBase_clean, current_style_font
	text = dialog.textEdit.document().toPlainText()
	file3 = open(urlBase_clean+"/tmp/common.css", "w")
	file3.write(text.replace('<FONT>', current_style_font))
	file3.close()
	dialog.webView.reload()


def clickSave():
	global dialog, urlBase_clean
	text = dialog.textEdit.document().toPlainText()
	#print(text)
	print('Sauvegarde css')
	file3 = open(urlBase_clean+"/ressources/common.css", "w")
	file3.write(text)
	file3.close()
	dialog.webView.reload()


def load_preset():
	global urlBase_clean, dialog2, window2
	dialog2 = presetUI.Ui_Dialog()
	window2 = QtGui.QDialog()
	dialog2.setupUi(window2)
	window2.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
	
	themes = []
	index = 0
	pos = 0
	for x in os.listdir(urlBase_clean+'/ressources/themes'):
		if os.path.isdir(urlBase_clean+'/ressources/themes/'+x) is False: 
			themes.append(x.replace('.css', ''))
			if x == 'default.css':
				pos = index
			index += 1
	dialog2.comboBox.clear()
	dialog2.comboBox.addItems(themes)
	dialog2.comboBox.setCurrentIndex(pos)
	
	dialog2.pushButton.clicked.connect(load_preset2)  # signal
	
	window2.exec_()


def load_preset2():
	global dialog, dialog2, window2
	style = dialog2.comboBox.currentText()
	print(style)
	
	file2  = open(urlBase_clean+"/ressources/themes/"+style+".css", "r")
	css = file2.read()
	file2.close()
	dialog.textEdit.setPlainText(css)
	
	window2.close()
	dialog2 = None
	window2 = None
	clickPreview()


class MyWindow(QtGui.QDialog):
	def closeEvent(self, event):
		event.ignore()
		result = QtGui.QMessageBox.question(self, "Confirm Exit...", "Are you sure you want to exit ?", QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
		
		if result == QtGui.QMessageBox.Yes:
			event.accept()


if __name__ == '__main__':
	myappid = 'wuxiaworld.epubcreator.qt4.2'  # arbitrary string
	if os.name == 'nt':
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
	app = QtGui.QApplication([])
	dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	app_icon = QtGui.QIcon()
	app_icon.addFile(dir+'/ressources/icon16x16.png', QtCore.QSize(16,16))
	app_icon.addFile(dir+'/ressources/icon24x24.png', QtCore.QSize(24,24))
	app_icon.addFile(dir+'/ressources/icon32x32.png', QtCore.QSize(32,32))
	app_icon.addFile(dir+'/ressources/icon48x48.png', QtCore.QSize(48,48))
	app_icon.addFile(dir+'/ressources/icon256x256.png', QtCore.QSize(256,256))
	app.setWindowIcon(app_icon)
	dialog = interface.Ui_Dialog()
	window = MyWindow()
	dialog.setupUi(window)
	window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
	
	dialog.radioButton_contentTable.clicked.connect(changePage)  # signal
	dialog.radioButton_chapter1.clicked.connect(changePage)  # signal
	dialog.pushButtonPreview.clicked.connect(clickPreview)  # signal
	dialog.pushButtonSave.clicked.connect(clickSave)  # signal
	dialog.presetButton.clicked.connect(load_preset)  # signal
	
	file1 = open(urlBase_clean+"/ressources/loading_fonts.txt", "r")
	file2 = open(urlBase_clean+"/ressources/common.css", "r")
	current_style_font = file1.read()
	css = file2.read()
	file1.close()
	file2.close()
	highlight = syntax.PythonHighlighter(dialog.textEdit.document())
	dialog.textEdit.setPlainText(css)
	highlight.rehighlight()
	
	highlightTimer = QtCore.QTimer()
	highlightTimer.timeout.connect(redoTextHighlight)
	highlightTimer.setInterval(200)
	highlightTimer.start()
	
	checkFontLastTime = float(os.path.getmtime(urlBase_clean+"/ressources/loading_fonts.txt"))
	checkFontTimer = QtCore.QTimer()
	checkFontTimer.timeout.connect(updateFont)
	checkFontTimer.setInterval(200)
	checkFontTimer.start()
	changePage()
	
	window.show()
	sys.exit(app.exec_())
