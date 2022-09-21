# encoding=utf-8
import sys
import time
import threading
from abc import abstractmethod

from PyQt5.QtWidgets import QFrame

"""
@author: v_jjyjiang 
@Description: TODO(这里用一句话描述这个模块的作用)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: custom_widgets.py
@time: 2018/8/3 19:46
"""


class CustomQFrame(QFrame):
    def __init__(self, parent):
        super(QFrame, self).__init__(parent)
        self.setAcceptDrops(True)
        self.__drag_listener = CustomQFrameListener()

    # self.setDragDropMode(QAbstractItemView.InternalMove)
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(QFrame, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(QFrame, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                # print(str(url.toLocalFile()))
                self.__drag_listener.get_drag_file_uri(self, url.toLocalFile())
                event.acceptProposedAction()

    def set_drag_listener(self, listener):
        self.__drag_listener = listener


class CustomQFrameListener(object):
    @abstractmethod
    def get_drag_file_uri(self, parent, file_uri):
        pass


if __name__ == '__main__':
    pass
