import abc
import os
from abc import abstractmethod

from PyQt5.QtCore import QAbstractListModel, QModelIndex
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QItemDelegate
from BaseLibrary.common_utils.listview.custom_list_ui import Ui_Dialog

"""
@author: jaey_jiang
@Description: TODO(自定义suffix_set配置添加器)
@contact: jaey_summer@qq.com
@software: PyCharm
@time: 2017/9/29 16:04
"""


# qtCreatorFile = "./res/suffix_set.data"  # Enter file here.
# Ui_MainWindow, QtBaseClass = loadUiType(qtCreatorFile)


class CustomListView(Ui_Dialog, QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        self.__title = "listview"
        self.setWindowTitle(self.__title)
        self.setFixedSize(320, 260)
        self.move(600, 300)
        self.btn_confirm.clicked.connect(lambda: self.__btn_confirm_data())
        # self.btn_cancel.clicked.connect(lambda: self.__btn_cancel_dialog())
        # self.btn_add_item.clicked.connect(lambda: self.__add_item())
        self.btn_delete.clicked.connect(lambda: self.__delete_item())
        # self.et_add_item.setText("")
        # 回调接口
        self.__list_selector_interface = None
        self.__list_data = []
        self.flag = None

    def set_title(self, title):
        """
        设置标题
        :param title: 
        :return: 
        """
        self.__title = title
        self.setWindowTitle(self.__title)

    def set_select_listener(self, listener):
        """
        设置回调接口
        :param listener:
        :return:
        """
        self.__list_selector_interface = listener

    def __add_item(self):
        """
        添加项
        :return:
        """
        # print u"添加"
        # add_item = self.et_add_item.text()
        # print(add_item)
        # add_item = add_item.replace(" ", "")
        # self.__list_data.append(add_item)
        file_set = open(os.getcwd() + "/res/data_select.ini", "w+")
        for file_name in self.__list_data:
            file_set.write("data = %s\n" % file_name)
        file_set.close()
        # self.set_data(self.__list_data)

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
        self.set_data(self.flag,self.__list_data)
        file_set = open(os.getcwd() + "/res/data_select.ini", "w+")
        for file_name in self.__list_data:
            file_set.write("data = %s\n" % file_name)
        file_set.close()

    def set_data(self, flag,  list_data):
        """
        设置数据
        :return:
        """
        # 写入文件
        self.__add_item()
        self.flag = flag
        self.__list_data = list_data
        listmode = CustomListModel(self.__list_data, self)
        de = CustomListDelegate(self)
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
        item_list = []
        self.lv_data.selectAll()
        for q in self.lv_data.selectedIndexes():
            # print q.data().toString()
            item_list.append(q.data())
            # print v
            # print v.toPyObject()
            # print str(q.data(q.row()).toString())
        self.__list_selector_interface.get_selected_list_success(self.flag,item_list)
        self.close()

    def show_listview(self):
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

    def get_historical_data(self):
        if os.path.exists(os.getcwd() + "/res/data_select.ini"):
            file = open(os.getcwd() + "/res/data_select.ini", "r")
            for line in file.readlines():
                pass
                #print(line)
                # return
            file.close()


class CustomListDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    # def paint(self, painter, option, index):
    #     painter.save()
    #
    #     # set background color
    #     painter.setPen(QPen(Qt.NoPen))
    #     if option.state & QStyle.State_Selected:
    #         painter.setBrush(QBrush(Qt.gray))
    #     else:
    #         painter.setBrush(QBrush(Qt.white))
    #     painter.drawRect(option.rect)
    #
    #     # set text color
    #     painter.setPen(QPen(Qt.black))
    #     value = index.data(Qt.DisplayRole)
    #     if value is not None:
    #         text = value
    #         painter.drawText(option.rect, Qt.AlignLeft, text)
    #
    #     painter.restore()

    def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
        super().paint(QPainter, QStyleOptionViewItem, QModelIndex)


class CustomListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QAbstractListModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == 0:
            return self.listdata[index.row()]
        else:
            return None


class CustomListInterface(object):
    @abc.abstractmethod  # 抽象方法
    def get_selected_list_success(self, flag, list_item):
        pass
