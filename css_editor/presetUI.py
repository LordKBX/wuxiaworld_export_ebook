# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'presetUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 60)
        Dialog.setMinimumSize(QtCore.QSize(400, 60))
        Dialog.setMaximumSize(QtCore.QSize(400, 60))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(80, 30))
        self.label.setStyleSheet("background-color: rgb(204, 204, 204);padding-left:5px;")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 30))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(80, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(80, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Load Preset Theme", None))
        self.label.setText(_translate("Dialog", "Preset", None))
        self.pushButton.setText(_translate("Dialog", "&Validate", None))

