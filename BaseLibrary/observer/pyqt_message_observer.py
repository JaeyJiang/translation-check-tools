# encoding=utf-8
import argparse

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from BaseLibrary.observer.message_observer import PropertyObservable

"""
@author: v_jjyjiang 
@Description: TODO(这里用一句话描述这个模块的作用)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: pyqt_message_observer.py
@time: 2018/5/11 22:44
"""


class PyQtPropertyObservable(PropertyObservable):
    def __init__(self):
        super().__init__()
        self.__list_py_thread = []
        a = "aaaa"

    def __str__(self):
        return super().__str__()

    def __del__(self):
        pass

    def run_pyqt_thread(self, run_thread, function_args=()):
        """
          传入的线程走完必须给一个return
          :param run_thread: 
          :param function_args: 
          :return: sender, callback_code 
        """
        # print(function_args)
        my_t = ObserverHandler(run_thread, function_args)
        my_t.finishSignal.connect(self.__thread_callback)
        my_t.start()
        self.__list_py_thread.append(my_t)
        return my_t

    def __thread_callback(self, result):
        # print(result[0])
        # print(result[1])
        if len(result) == 2:
            result[0].fire_event(result[0], result[1])
        elif len(result) == 3:
            result[0].fire_event(result[0], result[1], result[2])
            # print(result[2])


class ObserverHandler(QThread):
    def __init__(self, run_thread, args, parent=None, ):
        # super(ObserverHandler, self).__init__(parent)
        # print(args)
        super().__init__(parent)
        self.run_thread = run_thread
        self.args = args

    finishSignal = QtCore.pyqtSignal(tuple)

    def qt_fire_event(self, result=()):
        """
        线程运行时的回调
        :param result: 
        :return: 
        """
        self.finishSignal.emit(result)

    def run(self):
        """
        # 线程结束时的回调
        :return:
        """
        self.finishSignal.emit(self.run_thread(*self.args))


if __name__ == '__main__':
    pass
