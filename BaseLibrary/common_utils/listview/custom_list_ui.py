# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'custom_list_ui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 258)
        self.btn_confirm = QtWidgets.QPushButton(Dialog)
        self.btn_confirm.setGeometry(QtCore.QRect(20, 220, 75, 31))
        self.btn_confirm.setObjectName("btn_confirm")
        self.lv_data = QtWidgets.QListView(Dialog)
        self.lv_data.setGeometry(QtCore.QRect(0, 0, 401, 211))
        self.lv_data.setObjectName("lv_data")
        self.btn_delete = QtWidgets.QPushButton(Dialog)
        self.btn_delete.setGeometry(QtCore.QRect(180, 220, 111, 31))
        self.btn_delete.setObjectName("btn_delete")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_confirm.setText(_translate("Dialog", "confirm"))
        self.btn_delete.setText(_translate("Dialog", "delete_selected"))

