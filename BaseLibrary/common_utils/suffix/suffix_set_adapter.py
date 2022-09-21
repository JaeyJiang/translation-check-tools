# encoding=utf-8
import sys
import time
import threading

from PyQt5.QtCore import QAbstractListModel, QModelIndex
from PyQt5.QtWidgets import QItemDelegate

"""
@author: v_jjyjiang 
@Description: TODO(这里用一句话描述这个模块的作用)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: file_list_adapter.py
@time: 2017/9/29 16:14
"""


class SuffixSetDelegate(QItemDelegate):
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


class SuffixSetListModel(QAbstractListModel):
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
