# encoding=utf-8
import threading
import time

from BaseLibrary.observer.pyqt_message_observer import PyQtPropertyObservable
from core.tc_tools_new import TCTProgressListener

"""
@author: v_jjyjiang 
@Description: TODO(这里用一句话描述这个模块的作用)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: base_logic.py
@time: 2018/5/11 18:52
"""


class TCTBaseLogic(PyQtPropertyObservable, TCTProgressListener):
    success_report_finished = 0x0001
    success_progress = 0x0002

    def __init__(self):
        super().__init__()
        self.__tc_tools = None
        self.__report_handler = None

    def __str__(self):
        return super().__str__()

    def __del__(self):
        pass

    def get_report_for_tc_tools(self, report_name, tc_tools):
        self.__tc_tools = tc_tools
        self.__tc_tools.set_progress_listener(self)
        self.__report_handler = self.run_pyqt_thread(run_thread=self.__run_start_filter,
                                                     function_args=(report_name,))

    def __run_start_filter(self, report_name):
        report_uri = self.__tc_tools.start_filter(report_name)
        return self, self.success_report_finished, [report_uri]
        # self.fire_event(self, self.success, ["成功", "12", 1, "33"])

    def get_progress_data(self, parent, progress_data):
        if parent == self.__tc_tools:
            # print(progress_data)
            self.__report_handler.qt_fire_event(result=(self, self.success_progress, (progress_data[0], progress_data[1])))


if __name__ == '__main__':
    pass
