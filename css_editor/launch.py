from PyQt4 import QtCore, QtGui
import sys
import os
import ctypes
import interface

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

if __name__ == '__main__':
	myappid = 'wuxiaworld.epubcreator.qt4.2' # arbitrary string
	if os.name == 'nt': ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
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
	window = QtGui.QDialog()
	dialog.setupUi(window)
	window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
	dialog.main()
	sys.exit(app.exec_())
