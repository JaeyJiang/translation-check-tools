import abc
import os

import sys
from PyQt5 import QtWidgets, QtCore
from abc import abstractmethod

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem, QApplication, QFrame

"""
@author: jaey_jiang
@Description: TODO(自定义listview checkbox)
@contact: jaey_summer@qq.com
@software: PyCharm
@time: 2017/9/29 16:04
"""


# qtCreatorFile = "./res/suffix_set.data"  # Enter file here.
# Ui_MainWindow, QtBaseClass = loadUiType(qtCreatorFile)


class CustomCheckBox(QtWidgets.QWidget):
    def __init__(self, title, list_data=None, default_checked=[]):
        super().__init__()
        self.__listener = None
        self.__list_selected = []  # 已经选择的按钮
        self.move(520, 280)
        # resize()方法调整窗口的大小。(宽,高)
        self.resize(550, 0)
        self.__layout = QtWidgets.QVBoxLayout()
        # self.lMessage = QtWidgets.QLabel(self)
        self.btn_confirm = QtWidgets.QPushButton(self)
        # self.btn_confirm.setGeometry(QtCore.QRect(0, 0,500,500))

        self.setWindowTitle(title)
        self.__default_checked = default_checked
        if list_data is None:
            self.__items = ['Python', 'Golang', 'JavaScript', 'C', 'C++', 'PHP']
        else:
            self.__items = list_data
        for index in range(len(self.__items)):
            checkBox = QtWidgets.QCheckBox(self.__items[index], self)
            checkBox.id_ = index
            checkBox.stateChanged.connect(self.__check)  # 1
            if (len(self.__default_checked)) > 0 and (index in self.__default_checked):
                checkBox.setChecked(True)
            self.__layout.addWidget(checkBox)

        self.btn_confirm.setText("确定")
        self.btn_confirm.clicked.connect(lambda: self.__btn_confirm())
        # layout.addWidget(self.lMessage)
        self.__layout.addWidget(self.btn_confirm)
        self.setLayout(self.__layout)

    def set_listener(self, listener):
        self.__listener = listener

    def __btn_confirm(self):
        self.__listener.get_custom_check_box(self.__list_selected, self)
        self.close()

    def __check(self, state):
        checkBox = self.sender()
        if state == QtCore.Qt.Unchecked:
            self.__list_selected.remove(checkBox.id_)
            # print(u'取消选择了{0}: {1}'.format(checkBox.id_, checkBox.text()))
            # self.lMessage.setText(u'取消选择了{0}: {1}'.format(checkBox.id_, checkBox.text()))
        elif state == QtCore.Qt.Checked:
            self.__list_selected.append(checkBox.id_)
            # print(u'选择了{0}: {1}'.format(checkBox.id_, checkBox.text()))
            # self.lMessage.setText(u'选择了{0}: {1}'.format(checkBox.id_, checkBox.text()))


class CustomCheckBoxListener(object):
    @abstractmethod
    def get_custom_check_box(self, list_tuple, sender):
        """
        接口
        :param list_tuple: 
        :param sender: 发送者自己
        """
        pass


"""
下拉列表复选框
"""
class ComboCheckBox(QComboBox):
    def __init__(self):  # items==[str,str...]
        super().__init__()
        self.__items = []
        self.__row_num = 0
        self.__selected_row_num = 0
        self.__q_checkbox_list = []
        self.__q_line_edit = QLineEdit()
        self.__q_line_edit.setReadOnly(True)
        self.__q_list_widget = QListWidget()

    def set_list_data(self, items):
        self.__items = items
        self.__items.insert(0, '全部')
        self.__row_num = len(self.__items)
        self.__add_qcheckbox(0)
        self.__q_checkbox_list[0].stateChanged.connect(self.select_all)
        for i in range(1, self.__row_num):
            self.__add_qcheckbox(i)
            self.__q_checkbox_list[i].stateChanged.connect(self.show)
        self.setModel(self.__q_list_widget.model())
        self.setView(self.__q_list_widget)
        self.setLineEdit(self.__q_line_edit)

    def __add_qcheckbox(self, i):
        self.__q_checkbox_list.append(QCheckBox())
        qItem = QListWidgetItem(self.__q_list_widget)
        self.__q_checkbox_list[i].setText(self.__items[i])
        self.__q_list_widget.setItemWidget(qItem, self.__q_checkbox_list[i])

    def select_list(self):
        outputlist = []
        for i in range(1, self.__row_num):
            if self.__q_checkbox_list[i].isChecked():
                outputlist.append(self.__q_checkbox_list[i].text())
        self.__selected_row_num = len(outputlist)
        return outputlist

    def show(self):
        show = ''
        outputlist = self.select_list()
        self.__q_line_edit.setReadOnly(False)
        self.__q_line_edit.clear()
        for i in outputlist:
            show += i + ';'
        if self.__selected_row_num == 0:
            self.__q_checkbox_list[0].setCheckState(0)
        elif self.__selected_row_num == self.__row_num - 1:
            self.__q_checkbox_list[0].setCheckState(2)
        else:
            self.__q_checkbox_list[0].setCheckState(1)
        self.__q_line_edit.setText(show)
        self.__q_line_edit.setReadOnly(True)

    def select_all(self, state):
        if state == 2:
            for i in range(1, self.__row_num):
                self.__q_checkbox_list[i].setChecked(True)
        elif state == 1:
            if self.__selected_row_num == 0:
                self.__q_checkbox_list[0].setCheckState(2)
        elif state == 0:
            self.clear()

    def clear(self):
        for i in range(self.__row_num):
            self.__q_checkbox_list[i].setChecked(False)


if __name__ == '__main__':
    """
      window主函数
      """
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    # pyqt的QMainwWindow类的实体
    window = QFrame()
    # a = ComboCheckBox()
    # a.set_list_data(["1", "2", "3", "4", "5"])
    # a.show_a()
    # a.show()
    a = CustomCheckBox()
    a.set_data("asd",["1", "2", "3", "4", "5"])
    a.show()

    # resize()方法调整窗口的大小。(宽,高)
    window.resize(1000, 750)
    # move()方法移动窗口在屏幕上的位置到(x,y)坐标。
    window.move(450, 200)
    # 设置窗口最大的大小 (宽,高)
    # window.setFixedSize(1280, 720)
    # 从布局文件中加载ui界面
    # loadUi('./res/main_activity.ui', window)
    # 设置窗口的标题
    window.setWindowTitle("IP地址检查工具")
    # 设置窗口的图标，引用当前目录下的web.png图片
    window.setWindowIcon(QIcon('./res/tc_icon.png'))
    # 窗口显示
    window.show()
    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())
