# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1200, 768)
        Dialog.setMinimumSize(QtCore.QSize(1200, 768))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
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
        self.horizontalLayout_4.addWidget(self.radioButton_chapter1)
        spacerItem1 = QtGui.QSpacerItem(320, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.webView = QtWebKit.QWebView(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
        self.webView.setSizePolicy(sizePolicy)
        self.webView.setMinimumSize(QtCore.QSize(400, 720))
        self.webView.setMaximumSize(QtCore.QSize(600, 16777215))
        self.webView.setStyleSheet(_fromUtf8("background-color: rgb(230, 230, 230);"))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.horizontalLayout_5.addWidget(self.webView)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(80, 30))
        self.label_2.setMaximumSize(QtCore.QSize(80, 30))
        self.label_2.setAutoFillBackground(False)
        self.label_2.setStyleSheet(_fromUtf8("background-color: rgb(117, 117, 117);\n"
"color: rgb(255, 255, 255);\n"
"padding-left:6px;"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_8.addWidget(self.label_2)
        spacerItem2 = QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Dialog)
        self.plainTextEdit.setMinimumSize(QtCore.QSize(300, 720))
        self.plainTextEdit.setAcceptDrops(False)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
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
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButtonPreview = QtGui.QPushButton(Dialog)
        self.pushButtonPreview.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButtonPreview.setObjectName(_fromUtf8("pushButtonPreview"))
        self.horizontalLayout_2.addWidget(self.pushButtonPreview)
        self.pushButtonSave = QtGui.QPushButton(Dialog)
        self.pushButtonSave.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButtonSave.setObjectName(_fromUtf8("pushButtonSave"))
        self.horizontalLayout_2.addWidget(self.pushButtonSave)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setMinimumSize(QtCore.QSize(500, 720))
        self.textEdit.setMaximumSize(QtCore.QSize(600, 16777215))
        self.textEdit.setStyleSheet(_fromUtf8("background-color: rgb(220, 220, 220);"))
        self.textEdit.setFrameShape(QtGui.QFrame.NoFrame)
        self.textEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.textEdit.setLineWidth(0)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
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
        self.label_2.setText(_translate("Dialog", "HTML code", None))
        self.label.setText(_translate("Dialog", "CSS Style", None))
        self.pushButtonPreview.setText(_translate("Dialog", "&Preview", None))
        self.pushButtonSave.setText(_translate("Dialog", "Save", None))

from PyQt4 import QtWebKit
