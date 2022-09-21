# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sample_dialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(369, 192)
        self.dialog_confirm = QtWidgets.QPushButton(Dialog)
        self.dialog_confirm.setGeometry(QtCore.QRect(140, 142, 91, 31))
        self.dialog_confirm.setObjectName("dialog_confirm")
        self.le_dialog_message = QtWidgets.QLabel(Dialog)
        self.le_dialog_message.setGeometry(QtCore.QRect(40, 30, 301, 71))
        self.le_dialog_message.setObjectName("le_dialog_message")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.dialog_confirm.setText(_translate("Dialog", "确定"))
        self.le_dialog_message.setText(_translate("Dialog", "TextLabel"))

