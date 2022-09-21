# encoding=utf-8
import abc
import sys
import time
import subprocess
import threading
import os
import win32api
from abc import abstractmethod

from PyQt5.QtWidgets import QWidget, QFileDialog

"""
@author: jaey_jiang
@Description: TODO(这里用一句话描述这个模块的作用)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: file_manager.py
"""


class QFileManager(QWidget):
    def __init__(self, parent=None, *args):
        super(QFileManager, self).__init__(parent, *args)
        self.__default_uri = "D://"
        self.move(600, 300)
        self.listener = None

    def set_file_select_listener(self, listener):
        self.listener = listener

    def get_file_path(self, code=0):
        """
        获取文件的路径
        :return:
        """
        # absolute_path is a QString object
        # absolute_path = QFileDialog.getOpenFileName(self, "Open file",
        #                                             '.',
        #                                             "xml files (*.xml);;apk files (*.apk);;ipa "
        #                                             "files (*.ipa)")
        if code == 1:
            # absolute_path is a QString object
            absolute_path = QFileDialog.getOpenFileName(self, "Open  file",
                                                        '.',
                                                        "apk files (*.apk);;xml files (*.xml);;ipa files (*.ipa)")
        elif code == 2:
            # absolute_path is a QString object
            absolute_path = QFileDialog.getOpenFileName(self, "Open file",
                                                        '.',
                                                        "ipa files (*.ipa);;xml files (*.xml);;apk files (*.apk)")
        elif code == 3:
            # absolute_path is a QString object
            absolute_path = QFileDialog.getOpenFileName(self, "Select Excel File",
                                                        '.',
                                                        "Excel files (*.xls *.xlsx)")
        else:
            # absolute_path is a QString object
            absolute_path = QFileDialog.getOpenFileName(self, "Open file",
                                                        '.',
                                                        "xml files (*.xml);;apk files (*.apk);;ipa files (*.ipa)")

        print("select_file_uri:{0:s}\nselect_file_type:{1:s}".format(absolute_path[0],
                                                                     absolute_path[1]))
        absolute_path = absolute_path[0]
        return absolute_path
        # if absolute_path:
        #     cur_path = QDir('.')
        #     relative_path = cur_path.relativeFilePath(absolute_path)
        #
        #     print relative_path

    def get_dir_path(self):
        """
        获取文件夹的路径
        :return:
        """
        absolute_path = QFileDialog.getExistingDirectory(self, "choose directory",
                                                         self.__default_uri)

        self.__default_uri = absolute_path
        return absolute_path

    def get_files_path(self):
        """
        获取多个文件的路径
        :return:
        """
        path = QFileDialog.parent()

    def open_txt(self, uri):
        """
        打开一个xml文件
        :return:
        """
        if len(uri) > 1:
            t = threading.Thread(target=self.__open_thread_txt, args=(uri,))
            t.setDaemon(True)
            t.start()
            # win32api.ShellExecute(0, "open", "notepad.exe", uri, "", 1)

        pass

    def open_txt_list(self, uri_list):
        """
        打开多个xml文件
        :return:
        """
        print(len(uri_list))
        for uri in uri_list:
            if len(uri) > 1:
                t = threading.Thread(target=self.__open_thread_txt, args=(uri,))
                t.setDaemon(True)
                t.start()
                # win32api.ShellExecute(0, "open", "notepad.exe", uri, "", 1)
                pass

    def open_folder(self, uri):
        """
        开个线程打开文件夹
        :param uri: 
        :return: 
        """
        # print(uri)
        if len(uri) > 1:
            t = threading.Thread(target=self.__open_folder, args=(uri,))
            t.setDaemon(True)
            t.start()
            # win32api.ShellExecute(0, "open", "notepad.exe", uri, "", 1)

    def open_excel(self, uri):
        """
        打开Excel文件
        """
        if len(uri) > 1:
            t = threading.Thread(target=self.__open_thread_excel, args=(uri,))
            t.setDaemon(True)
            t.start()
            # t = threading.Thread(target=self.__open_thread_excel, args=(uri,))
            # t.setDaemon(True)
            # t.start()

    def delete_file(self, path):
        """
        删除文件
        :return:
        """
        os.remove(path)

    def __open_thread_txt(self, uri):
        """
        开个线程去跑命令行
        """
        # os.system("notepad %s" % uri)

        # si = subprocess.STARTUPINFO()
        # si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # mProcess = subprocess.Popen("notepad %s" % uri, stdin=subprocess.PIPE,
        #                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                             universal_newlines=True)
        # mProcess.stdout.readlines()
        # mProcess.wait()
        # mProcess = subprocess.Popen("", stdin=subprocess.PIPE,
        #                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                             universal_newlines=True)
        win32api.ShellExecute(0, "open", "notepad.exe", uri, "", 1)
        #lines = os.popen("notepad %s" % uri).readlines()
        # print lines

    def __open_thread_excel(self, uri):
        """
        打开文件
        """
        # uri = "D:\Python_Project\Python3_Tools\Translation_Check_Tools//result//data_result_4.xls"
        # lines = os.popen("%s" % uri).readlines()
        # win32api.ShellExecute(0, "open", "notepad.exe", uri, "", 1)
        win32api.ShellExecute(0, "open", uri, None, "", 1)
        # print lines

    def __open_folder(self, uri):
        """
        打开文件夹
        :param uri: 
        :return: 
        """
        print(uri)
        try:
            win32api.ShellExecute(0, "open", "explorer.exe", uri, "", 1)
        except Exception as e:
            print(e)


class FileSelectorInterface(object):
    """
    文件选择完后的回调接口
    """

    @abc.abstractmethod
    def get_select_file_name(self, file_names):
        pass
