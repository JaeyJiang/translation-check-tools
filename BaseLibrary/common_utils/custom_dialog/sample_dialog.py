# encoding=utf-8
from distutils.filelist import FileList
from PyQt5.QtWidgets import QDialog, QWidget
from BaseLibrary.common_utils.custom_dialog.sample_dialog_ui import Ui_Dialog

"""
@author: Jaey_Jiang
@Description: TODO(这里用一句话描述这个模块的作用)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: sample_dialog.py
"""


# qtCreatorFile = "./res/sample_dialog.data"
# Ui_MainWindow, QtBaseClass = loadUiType(qtCreatorFile)

class SampleDialog(Ui_Dialog,QDialog, QWidget):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.move(600, 300)
        # self.setFixedSize(300, 200)
        # self.quit = QtGui.QPushButton("Quit", self)
        # self.quit.setGeometry(62, 40, 75, 30)
        # self.quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        # self.connect(self.quit, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))
        file_list = FileList()

    def set_message(self, message, show_quit=True):
        """
        :return:
        """

        self.le_dialog_message.setText(message)
        if not show_quit:
            self.dialog_confirm.setVisible(False)
        self.dialog_confirm.clicked.connect(lambda: self.__quit())
        self.show()

    def __quit(self):
        self.close()
