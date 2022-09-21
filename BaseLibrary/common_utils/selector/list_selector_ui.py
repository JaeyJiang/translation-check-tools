# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'list_selector_ui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(402, 252)
        self.btn_confirm = QtWidgets.QPushButton(Dialog)
        self.btn_confirm.setGeometry(QtCore.QRect(40, 220, 75, 23))
        self.btn_confirm.setObjectName("btn_confirm")
        self.btn_cancel = QtWidgets.QPushButton(Dialog)
        self.btn_cancel.setGeometry(QtCore.QRect(160, 220, 75, 23))
        self.btn_cancel.setObjectName("btn_cancel")
        self.lv_data = QtWidgets.QListView(Dialog)
        self.lv_data.setGeometry(QtCore.QRect(0, 0, 401, 211))
        self.lv_data.setObjectName("lv_data")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_confirm.setText(_translate("Dialog", "确定"))
        self.btn_cancel.setText(_translate("Dialog", "取消"))

