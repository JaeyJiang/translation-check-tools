# encoding=utf-8
import os
import sys
import time
import threading

"""
@author: v_jjyjiang 
@Description: TODO(这里用一句话描述这个模块的作用)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: file_utils.py
"""


class FileUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def copyFiles(sourceDir, targetDir):
        if sourceDir.find(".svn") > 0:
            return
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir, file)
            targetFile = os.path.join(targetDir, file)
            if os.path.isfile(sourceFile):
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)
                if not os.path.exists(targetFile) or (os.path.exists(targetFile) and (
                            os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
