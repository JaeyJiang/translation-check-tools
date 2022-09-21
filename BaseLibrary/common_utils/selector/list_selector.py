# encoding=utf-8
import abc

from PyQt5.QtWidgets import QWidget, QAbstractItemView

from BaseLibrary.common_utils.selector.list_selector_adapter import ListSelectorListModel, \
    ListSelectorDelegate
from BaseLibrary.common_utils.selector.list_selector_ui import Ui_Dialog

"""
@author: jaey_jiang
@Description: TODO(自定义选择器,需要传入选择的列表的地址)
@contact: jaey_summer@qq.com
@software: PyCharm
"""
# qtCreatorFile = "./res/list_selector.data"  # Enter file here.
# Ui_MainWindow, QtBaseClass = loadUiType(qtCreatorFile)


class ListSelector(Ui_Dialog, QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        title = u"请选择配置文件中需要对比的列"
        self.setWindowTitle(title)
        self.setFixedSize(400, 250)
        self.move(600, 300)
        self.btn_confirm.clicked.connect(lambda: self.__btn_confirm_data())
        self.btn_cancel.clicked.connect(lambda: self.__btn_cancel_dialog())
        # 用来做接口的标识
        self.__flag = -1
        # 回调接口
        self.__list_selector_interface = None

    def set_list_listener(self, listener):
        """
        设置回调接口
        :param listener:
        :return:
        """
        self.__list_selector_interface = listener

    def set_data(self, flag, list_data):
        """
        设置数据
        :return:
        """
        self.__flag = flag
        listmode = ListSelectorListModel(list_data, self)
        de = ListSelectorDelegate(self)
        self.lv_data.setModel(listmode)
        self.lv_data.setItemDelegate(de)
        self.lv_data.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置选择模式

    def __btn_confirm_data(self):
        """
        提交选择的文件路径
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
        list_data = []
        for q in self.lv_data.selectedIndexes():
            # print q.data().toString()
            string = q.data()
            # result = chardet.detect(string)
            # if not (result["encoding"] == "utf-8"):
            #     string = string.decode("gbk", "ignore")
            #     string = string.encode("utf-8", "ignore")
            # string = string.decode("utf-8")
            list_data.append(string)
            #list_index.append(self.lv_data)

        self.__list_selector_interface.get_list_data(self.__flag, list_data)
        self.close()

    def show_list_selector(self):
        """
        显示这个文件选择器
        :return:
        """
        # print dir_uri
        self.show()

    def __btn_cancel_dialog(self):
        """
        关闭选择框
        :return:
        """
        self.close()


class ListSelectorInterface(object):
    @abc.abstractmethod  # 抽象方法
    def get_list_data(self, flag, list_data):
        pass
