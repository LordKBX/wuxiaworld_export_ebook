import PyQt4
import PyQt4.QtCore
import PyQt4.QtGui
import PyQt4.QtWebKit
import PyQt4.QtNetwork
import sys
import interface

try:
    _fromUtf8 = PyQt4.QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

if __name__ == '__main__':
	app = PyQt4.QtGui.QApplication([])
	dialog = interface.Ui_Dialog()
	dialog.setupUi(PyQt4.QtGui.QDialog())
	dialog.main()
	sys.exit(app.exec_())
