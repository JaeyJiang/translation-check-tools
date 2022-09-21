import abc
import os
from abc import abstractmethod

from PyQt5.QtWidgets import QWidget, QAbstractItemView

from BaseLibrary.common_utils.suffix.suffix_set_adapter import SuffixSetListModel, SuffixSetDelegate
from BaseLibrary.common_utils.suffix.suffix_set_ui import Ui_Dialog

"""
@author: jaey_jiang
@Description: TODO(自定义suffix_set配置添加器)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: suffix_set.py
@time: 2017/9/29 16:04
"""


# qtCreatorFile = "./res/suffix_set.data"  # Enter file here.
# Ui_MainWindow, QtBaseClass = loadUiType(qtCreatorFile)


class SuffixSet(Ui_Dialog, QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        self.__title = u"SuffixSet"
        self.setWindowTitle(self.__title)
        self.setFixedSize(400, 300)
        self.btn_confirm.clicked.connect(lambda: self.__btn_confirm_data())
        self.btn_cancel.clicked.connect(lambda: self.__btn_cancel_dialog())
        self.btn_add_item.clicked.connect(lambda: self.__add_item())
        self.btn_delete.clicked.connect(lambda: self.__delete_item())
        self.et_add_item.setText("")
        # 回调接口
        self.__files_selector_interface = None
        self.__list_data = []

    def set_files_listener(self, listener):
        """
        设置回调接口
        :param listener:
        :return:
        """
        self.__files_selector_interface = listener

    def __add_item(self):
        """
        添加项
        :return:
        """
        # print u"添加"
        add_item = self.et_add_item.text()
        # print(add_item)
        add_item = add_item.replace(" ", "")
        self.__list_data.append(add_item)
        file_set = open(os.getcwd() + "/res/suffix.ini", "w+")
        for file_name in self.__list_data:
            file_set.write("LN = %s\n" % file_name)
        file_set.close()
        self.set_data(self.__list_data)

        # 下面这个方式是必须指定.xxx
        # index = add_item.find(".")
        # if index == 0:
        #     self.__list_data.append(add_item)
        #     file_set = open(os.getcwd() + "/res/suffix.ini", "w+")
        #     for file_name in self.__list_data:
        #         file_set.write("LN = %s\n" % file_name)
        #     file_set.close()
        #     self.set_data(self.__list_data)

    def __delete_item(self):
        """
        删除项
        :return:
        """
        # print u"删除"
        data_list = []
        for q in self.lv_data.selectedIndexes():
            # print q.data().toString()
            data_list.append(q.data())
            # print v
            # print v.toPyObject()
            # print str(q.data(q.row()).toString())
        for delete in data_list:
            self.__list_data.remove(delete)
        self.set_data(self.__list_data)
        file_set = open(os.getcwd() + "/res/suffix.ini", "w+")
        for file_name in self.__list_data:
            file_set.write("LN = %s\n" % file_name)
        file_set.close()

    def set_data(self, list_data):
        """
        设置数据
        :return:
        """
        self.__list_data = list_data
        listmode = SuffixSetListModel(self.__list_data, self)
        de = SuffixSetDelegate(self)
        self.lv_data.setModel(listmode)
        self.lv_data.setItemDelegate(de)
        self.lv_data.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置选择模式

    def __btn_confirm_data(self):
        """
        确定配置信息
        :return:
        """
        # print "post uri"
        # t = QModelIndex()
        # t.data()
        # t.
        # t.column()
        # t.
        # v = QVariant()
        # v.toString()
        # print self.lv_data.selectedIndexes()
        files_list = []
        for q in self.lv_data.selectedIndexes():
            # print q.data().toString()
            files_list.append(q.data())
            # print v
            # print v.toPyObject()
            # print str(q.data(q.row()).toString())
        self.__files_selector_interface.set_suffix_success(files_list)
        self.close()

    def show_suffix_set(self):
        """
        显示这个控件
        :return:
        """
        # print dir_uri
        self.show()

    def __btn_cancel_dialog(self):
        """
        关闭控件
        :return:
        """
        self.close()


class SuffixSetInterface(object):

    @abstractmethod  # 抽象方法
    def set_suffix_success(self, files_name):
        raise NotImplementedError("你必须实现抽象方法")
