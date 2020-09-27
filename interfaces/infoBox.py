# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'infoBox.ui'
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
        Dialog.resize(500, 104)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(500, 100))
        Dialog.setMaximumSize(QtCore.QSize(500, 104))
        Dialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Dialog.setWhatsThis("")
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label.setStyleSheet("background-image: url(:/root/info72x72.png);\n"
"background-repeat:no-repeat;\n"
"background-position:center;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(398, 65))
        self.label_2.setMaximumSize(QtCore.QSize(398, 65))
        font = QtGui.QFont()
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_2.setFont(font)
        self.label_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setStyleSheet("")
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(True)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(5, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_2.setText(_translate("Dialog", "INFO", None))
        self.pushButton.setText(_translate("Dialog", "&Ok", None))

import r_rc

