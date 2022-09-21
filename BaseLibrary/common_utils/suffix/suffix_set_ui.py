# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'suffix_set_ui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(402, 305)
        self.btn_confirm = QtWidgets.QPushButton(Dialog)
        self.btn_confirm.setGeometry(QtCore.QRect(40, 262, 75, 31))
        self.btn_confirm.setObjectName("btn_confirm")
        self.btn_cancel = QtWidgets.QPushButton(Dialog)
        self.btn_cancel.setGeometry(QtCore.QRect(130, 262, 75, 31))
        self.btn_cancel.setObjectName("btn_cancel")
        self.lv_data = QtWidgets.QListView(Dialog)
        self.lv_data.setGeometry(QtCore.QRect(0, 0, 401, 211))
        self.lv_data.setObjectName("lv_data")
        self.btn_add_item = QtWidgets.QPushButton(Dialog)
        self.btn_add_item.setGeometry(QtCore.QRect(170, 220, 75, 31))
        self.btn_add_item.setObjectName("btn_add_item")
        self.btn_delete = QtWidgets.QPushButton(Dialog)
        self.btn_delete.setGeometry(QtCore.QRect(240, 262, 111, 31))
        self.btn_delete.setObjectName("btn_delete")
        self.et_add_item = QtWidgets.QLineEdit(Dialog)
        self.et_add_item.setGeometry(QtCore.QRect(40, 220, 113, 31))
        self.et_add_item.setObjectName("et_add_item")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_confirm.setText(_translate("Dialog", "confirm"))
        self.btn_cancel.setText(_translate("Dialog", "cancel"))
        self.btn_add_item.setText(_translate("Dialog", "add"))
        self.btn_delete.setText(_translate("Dialog", "delete_selected"))

