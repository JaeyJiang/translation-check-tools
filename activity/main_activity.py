import json
import os
import sys
import xlrd
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QApplication, QMainWindow
from BaseLibrary.common_utils.checkbox.custom_checkbox import CustomCheckBox, CustomCheckBoxListener
from BaseLibrary.common_utils.custom_dialog.sample_dialog import SampleDialog
from BaseLibrary.common_utils.custom_widgets.custom_widgets import CustomQFrameListener
from BaseLibrary.common_utils.excel.excel_utils import ExcelUtils
from BaseLibrary.common_utils.file.file_manager import QFileManager
from BaseLibrary.common_utils.file.file_utils import FileUtils
from BaseLibrary.common_utils.listview.custom_listview import CustomListView, CustomListInterface
from BaseLibrary.common_utils.selector.list_selector import ListSelector, ListSelectorInterface
from BaseLibrary.common_utils.stringutils import StringUtils
from BaseLibrary.observer.message_observer import PropertyListener
from core.tc_tools_test import TC_Tools
from logic.base_logic import TCTBaseLogic
from res.main_activity_tct_ui import Ui_MainWindow
from PyQt5.uic import loadUiType

"""
@author: v_jjyjiang 
@Description: 检查翻译全配置文本
@contact: jaey_summer@qq.com
@software: PyCharm
@file: main_activity.py
"""


# qtCreatorFile = "./res/main_activity_ui.ui"
# Ui_MainWindow, QtBaseClass = loadUiType(qtCreatorFile)


class TCTMainActivity(QMainWindow, Ui_MainWindow, ListSelectorInterface, CustomListInterface, CustomCheckBoxListener,
                      CustomQFrameListener,
                      PropertyListener):
    def __init__(self):
        super(TCTMainActivity, self).__init__()

        self.logic = TCTBaseLogic()
        self.logic.add_listener(self, [TCTBaseLogic.success_report_finished, TCTBaseLogic.success_progress])

        self.setupUi(self)

        # 初始化控件
        self.__init_view()

        # Excel表格一的路径
        self.__select_dir_path_1 = ""

        # 打开的这个excel文件的对象
        self.__excel_data = None

        # 保存整个sheet对象的列表
        self.__list_sheet = []

        # 选择的sheet名
        self.__select_sheet_name = ""

        # 选择的sheet
        self.__select_sheet = None

        # 表格一的sheet的数据集
        self.__list_sheet_data_1 = []

        # 需要处理的列的数据集
        self.__list_col_data_1 = []

        # 选择基准的列的数据集
        self.__list_col_data_2 = []

        # 选择需要处理的列
        self.__excel_select_col_1 = []

        # 选择基准的列
        self.__excel_select_col_base = 0

        # 报告保存的路径
        self.__old_report_path = ""

        # 文件选择器
        self.__file_manager = QFileManager()

        # 接口标识,选择对比的列
        self.__flag_1 = 1

        # 接口表示,选择基准的列
        self.__flag_2 = 2

        # 接口表示 选择sheet
        self.__sheet_flag_1 = 3

        # 复制后的文件路径
        self.__xlsx_uri_1 = ""

        # sheet的列表选择器
        self.__list_sheet_selector_1 = ListSelector()
        self.__list_sheet_selector_1.set_list_listener(self)

        # 需要进行对比的列选择器一
        self.__list_selector_1 = ListSelector()
        self.__list_selector_1.set_list_listener(self)

        # 基准的列选择器
        self.__list_selector_2 = ListSelector()
        self.__list_selector_2.set_list_listener(self)

        # 需要打开的检查项列表
        self.__list_switch_check = []

        # 开始检查时的dialog
        self.__start_dialog = SampleDialog()

        # 译文长度检查的阈值
        self.__trans_threshold = 100

        # 运行时产生的各种dialog
        self.__run_dialog = SampleDialog()

        # 读取AOV检查指定字节长度配置文件后的配置数据
        self.__dict_length_conf = {"Key": [], "Length": []}

        # 各种默认路径Uri的存储配置
        self.__dict_uri_conf = {"excel_length_conf": ""}

        # 开关checkbox
        # ["开启漏翻检查",
        #  "开启标点符号检查,半角/全角是否一致或数量不一致等"
        #  "开启占位符问题(%),译文中的%后的标记与基准列的是否一致"
        #  "开启转义字符检查,包括其数量和一致性,如:'\\n',建议按需选择,减少误报",
        #  "存在标签检查,暂时只有'{}'标签",
        #  "开启html/xml中标签Name检查的,如:<xxxx><yyyy/>",
        #  "开启颜色十六进制标签的检查,包括数量和一致性,如:[ffffff]",
        #  "开启阿拉伯数字的检查,包括数量和一致性,如1, 100, 1000"]

        self.__dict_check_switch = {"0": ["开启漏翻检查", True],
                                    "1": ["开启标点符号检查,半角/全角是否一致或数量不一致等", True],
                                    "2": ["开启占位符问题(%),译文中的%后的标记与基准列的是否一致", True],
                                    "3": ["开启指定标签检查,暂时只检查'{}'标签", True],
                                    "4": ["开启转义字符检查,包括其数量和一致性,如:'\\n',建议按需选择,减少误报", True],
                                    "5": ["开启html/xml中标签Name检查,如:<xxxx><yyyy/>", True],
                                    "6": ["开启颜色十六进制标签的检查,包括数量和一致性,如:[ffffff]", True],
                                    "7": ["开启阿拉伯数字的检查,包括数量和一致性,如1, 100, 1000", True],
                                    "8": ["开启英文中是否包含中文的检查", True],
                                    "9": ["开启译文长度的检查(与基准参照文的阈值来比较)", True],
                                    "10": ["开启Key和文本头尾有空格或换行的检查", True],
                                    "11": ["开启根据配置文件检查指定Key对应的翻译长度", True]
                                    }
        self.__list_check_data = []
        for value in list(self.__dict_check_switch.values()):
            self.__list_check_data.append(value[0])
        # print(self.__list_check_data)
        # list_check_data = ["开启漏翻检查",
        #                    "开启标点符号检查,半角/全角是否一致或数量不一致等",
        #                    "开启占位符问题(%),译文中的%后的标记与基准列的是否一致",
        #                    "开启指定标签检查,暂时只检查'{}'标签",
        #                    "开启转义字符检查,包括其数量和一致性,如:'\\n',建议按需选择,减少误报",
        #                    "开启html/xml中标签Name检查,如:<xxxx><yyyy/>",
        #                    "开启颜色十六进制标签的检查,包括数量和一致性,如:[ffffff]",
        #                    "开启阿拉伯数字的检查,包括数量和一致性,如1, 100, 1000",
        #                    "开启英文中是否包含中文的检查",
        #                    "开启译文长度的检查(与基准参照文的阈值来比较)",
        #                    "开启Key和文本头尾有空格或换行的检查",
        #                    "开启AOV根据配置检查指定Key对应的翻译长度"
        #                    ]
        if not (os.path.exists(os.getcwd() + "/res/default_checked.json")):
            file = open(os.getcwd() + "/res/default_checked.json", "w+")
            json.dump(self.__dict_check_switch, file)
            file.close()
            for conf in self.__dict_check_switch.items():
                if conf[1][1]:
                    self.__list_switch_check.append(int(conf[0]))
        else:
            file = open(os.getcwd() + "/res/default_checked.json", "r+")
            try:
                temp = json.load(file)
                for conf in temp.items():
                    if conf[1][1]:
                        self.__list_switch_check.append(int(conf[0]))
                if 9 in self.__list_switch_check:  # 控制阈值显示框
                    self.lab_trans_threshold.setVisible(True)
                    self.et_trans_threshold.setVisible(True)
                else:
                    self.lab_trans_threshold.setVisible(False)
                    self.et_trans_threshold.setVisible(False)
            except Exception as e:
                print(e)
            finally:
                file.close()
            if 11 in self.__list_switch_check:  # 控制配置表选择Frame的显示
                self.frame_select_length_conf.setVisible(True)
                if not (os.path.exists(os.getcwd() + "/res/uri_conf.json")):
                    file = open(os.getcwd() + "/res/uri_conf.json", "w+")
                    json.dump(self.__dict_uri_conf, file)
                else:
                    file = open(os.getcwd() + "/res/uri_conf.json", "r+")
                    try:
                        self.__dict_uri_conf = json.load(file)
                        self.et_trans_length_conf.setText(self.__dict_uri_conf["excel_length_conf"])
                        if len(self.__dict_uri_conf["excel_length_conf"]) > 0:
                            # 选择完excel后,读取所有sheet表格到list
                            excel_length_conf_data = xlrd.open_workbook(self.__dict_uri_conf["excel_length_conf"])
                            sheet = excel_length_conf_data.sheet_by_index(0)  # 返回所有sheet的列表
                            list_col_1 = sheet.col_values(0)
                            list_col_2 = sheet.col_values(1)
                            self.__dict_length_conf["Key"] = list_col_1
                            self.__dict_length_conf["Length"] = list_col_2
                            print("加载地址配置:{uri_conf}".format(uri_conf=self.__dict_uri_conf))
                    except Exception as e:
                        print(e)
                    finally:
                        file.close()

            else:
                self.frame_select_length_conf.setVisible(False)
                # print(self.__list_switch_check)

        self.__check_box = CustomCheckBox("选择需要额外检查的项", list_data=self.__list_check_data,
                                          default_checked=self.__list_switch_check)
        self.__check_box.set_listener(self)

        # if not os.path.exists(os.getcwd() + "//cache"):
        #     os.makedirs(os.getcwd() + "//cache")
        # if not (os.path.exists(os.getcwd() + "/cache_data")):
        #     os.makedirs(os.getcwd() + "/cache_data")
        if not (os.path.exists(os.getcwd() + "/result")):
            os.makedirs(os.getcwd() + "/result")

        # 各种配置保存
        if not (os.path.exists(os.getcwd() + "/res/config.ini")):
            file = open(os.getcwd() + "/res/config.ini", "w")
            # 长度阈值保存
            self.et_trans_threshold.setText("100")
            file.write("Threshold=100")
            file.close()
        else:
            file = open(os.getcwd() + "/res/config.ini", "r")
            for temp in file.readlines():
                pos = temp.rfind("=")
                if not pos == -1:
                    key = temp[0:pos]
                    # 长度阈值读取
                    if key == "Threshold":
                        value = temp[pos + 1:]
                        self.__trans_threshold = int(value)
                        self.et_trans_threshold.setText(str(value))
            file.close()

    def __init_view(self):
        """
        初始化控件   
        :return:
        """
        # 保存文件名
        self.et_save_name.setText("data_result")

        # Excel表格一的目录
        self.et_dir_path_1.setText("")

        # 扫表格一的列
        self.et_base_col.setText("")

        # 扫描按钮
        self.btn_match.clicked.connect(lambda: self.on_click("start_match"))

        # 打开存储文件的按钮
        self.btn_open_file.clicked.connect(lambda: self.on_click("open_report"))

        # 选择Excel翻译表的按钮
        self.btn_select_dir_1.clicked.connect(lambda: self.on_click("select_excel_file"))

        # 需要对比的列选择按钮
        self.btn_compare_col.clicked.connect(lambda: self.on_click("select_excel_compare_col"))

        # 基准列的选择按钮
        self.btn_base_col.clicked.connect(lambda: self.on_click("select_base_col"))

        # 需要对比的列展示窗的显示
        self.btn_open_compare_list.clicked.connect(lambda: self.on_click("open_compare_listview"))
        # 先不显示它
        self.btn_open_compare_list.setVisible(False)

        # 选择翻译表Excel的sheet的按钮
        self.btn_sheet_select_1.clicked.connect(lambda: self.on_click("select_excel_sheet"))

        # 第一个Excel需要检查的sheet
        self.et_sheet_1.setText("")

        self.frame_select_length_conf.set_drag_listener(self)
        # 打开选择长度检查配置的文件选择器
        self.btn_select_length_conf.clicked.connect(lambda: self.on_click("select_length_conf"))

        # 打开日志文件
        self.btn_open_logs.clicked.connect(lambda: self.on_click("open_report_folder"))

        # 删除日志文件
        self.btn_delete_logs.clicked.connect(lambda: self.on_click("delete_logs"))
        self.btn_delete_logs.setVisible(False)

        # list compare 展示器
        self.__compare_listview = CustomListView()
        self.__compare_listview.set_title("已选择的列")
        self.__compare_listview.set_select_listener(self)

        # checkbox按钮
        self.btn_open_switch_check_list.clicked.connect(lambda: self.on_click("open_switch_check_list"))

        # 长度阈值输入框
        validator = QIntValidator()
        validator.setRange(0, 1000)
        self.et_trans_threshold.setValidator(validator)

        # 拖拽获取的文件地址监听接口
        self.frame_select_excel.set_drag_listener(self)

    def open_file(self):
        """
        打开报告文件
        :return:
        """
        # TODO
        self.__file_manager.open_excel(self.__old_report_path)

    def on_click(self, click_id):
        if click_id == "select_excel_file":
            """
            选择Excel翻译表的地址
            """
            self.__select_dir_path_1 = self.__file_manager.get_file_path(code=3)
            if len(self.__select_dir_path_1) > 0:
                self.et_dir_path_1.setText(self.__select_dir_path_1)
                self.__list_col_data_1 = []
                # 选择了新的地址以后就异常掉它
                self.btn_open_compare_list.setVisible(False)
                # 选择完excel后,读取所有sheet表格到list
                self.__excel_data = xlrd.open_workbook(self.__select_dir_path_1)
                self.__list_sheet = self.__excel_data.sheet_names()  # 返回所有sheet的列表
                # 清空各种数据
                self.__list_sheet_data_1 = self.__list_sheet
                self.__list_col_data_1 = []
                self.__list_col_data_2 = []
                self.__excel_select_col_1 = []
                self.__excel_select_col_base = 0
                self.__old_report_path = ""
                if self.__list_sheet is not None and len(self.__list_sheet) > 0:
                    self.__select_sheet_name = self.__list_sheet[0]
                    self.et_sheet_1.setText(self.__list_sheet[0])
                    self.__select_sheet = self.__excel_data.sheet_by_name(self.__select_sheet_name)
                self.et_base_col.setText("")

            else:
                self.__select_dir_path_1 = self.et_dir_path_1.text()
        if click_id == "select_length_conf":
            """
            选择检查翻译表长度Excel配置的地址
            """
            # 防止按关闭以后,会直接覆盖一个空的路径
            dict_uri_temp = self.__file_manager.get_file_path(code=3)
            # 保存地址
            if os.path.exists(os.getcwd() + "/res/uri_conf.json"):
                file = open(os.getcwd() + "/res/uri_conf.json", "w+")
                try:
                    json.dump(self.__dict_uri_conf, file)
                except Exception as e:
                    print(e)
                finally:
                    file.close()
            # 判断路径不是空的才加入配置
            if len(dict_uri_temp) > 0:
                self.__dict_uri_conf["excel_length_conf"] = dict_uri_temp
                self.et_trans_length_conf.setText(self.__dict_uri_conf["excel_length_conf"])
                # 选择完excel后,读取所有sheet表格到list
                excel_length_conf_data = xlrd.open_workbook(self.__dict_uri_conf["excel_length_conf"])
                sheet = excel_length_conf_data.sheet_by_index(0)  # 返回所有sheet的列表
                list_col_1 = sheet.col_values(0)
                list_col_2 = sheet.col_values(1)
                self.__dict_length_conf["Key"] = list_col_1
                self.__dict_length_conf["Length"] = list_col_2
            print("选择的长度检查配置地址:{uri_conf}".format(uri_conf=self.__dict_uri_conf))

        elif click_id == "select_excel_sheet":
            """
            选择excel表格一的sheet
            """
            # 复制文件操作
            # self.__copy_excel_cache()
            self.__list_sheet_data_1 = []
            if StringUtils.string_is_no_empty(self.__select_dir_path_1):
                try:
                    sheet_num = len(self.__list_sheet)
                    i = 0
                    # sheet 列表数据加载
                    while i < sheet_num:
                        data_temp = self.__list_sheet[i]
                        self.__list_sheet_data_1.append(data_temp)
                        i += 1
                    self.__list_sheet_selector_1.set_data(self.__sheet_flag_1, self.__list_sheet_data_1)
                    self.__list_sheet_selector_1.show_list_selector()
                    # print list_data.index(self.__excel_col_1)

                    # workbook.sheet_by_index(...)    #通过index来获得一个sheet对象，index从0开始算起
                    # workbook.sheet_by_name(...)    #根据sheet名获得相应的那个sheet对象
                except AttributeError as e:
                    print(e)
                    dialog = SampleDialog()
                    dialog.set_message("请先将Excel文件另存为09-2003版本!")
            else:
                dialog = SampleDialog()
                dialog.set_message("请先选择好需要操作的Excel文件!")
        elif click_id == "select_excel_compare_col":
            """
           选择需要对比的列
           :return:
           """
            # 复制文件操作
            # self.__copy_excel_cache()
            if StringUtils.string_is_no_empty(
                    self.__select_dir_path_1) and StringUtils.string_is_no_empty(
                self.__select_sheet_name):
                try:
                    self.__list_col_data_1 = []
                    sheet_col_num = self.__select_sheet.ncols
                    i = 0
                    while i < sheet_col_num:
                        data_temp = self.__select_sheet.cell(0, i).value
                        self.__list_col_data_1.append(data_temp)
                        i += 1
                    self.__list_selector_1.set_data(self.__flag_1, self.__list_col_data_1)
                    self.__list_selector_1.show_list_selector()
                    # print list_data.index(self.__excel_col_1)
                except AttributeError as e:
                    print(e)
                    dialog = SampleDialog()
                    dialog.set_message("请先选择正确的Excel文件!")
            else:
                dialog = SampleDialog()
                dialog.set_message("请先选择Excel文件,以及sheet表格!")
        elif click_id == "select_base_col":
            """
           选择基准的列
           :return:
           """
            # 复制文件操作
            # self.__copy_excel_cache()
            if StringUtils.string_is_no_empty(
                    self.__select_dir_path_1) and StringUtils.string_is_no_empty(
                self.__select_sheet_name):
                try:
                    self.__list_col_data_2 = []
                    sheet_col_num = self.__select_sheet.ncols
                    i = 0
                    while i < sheet_col_num:
                        data_temp = self.__select_sheet.cell(0, i).value
                        self.__list_col_data_2.append(data_temp)
                        i += 1
                    self.__list_selector_2.set_data(self.__flag_2, self.__list_col_data_2)
                    self.__list_selector_2.show_list_selector()
                    # print list_data.index(self.__excel_col_1)
                except AttributeError as e:
                    print(e)
                    dialog = SampleDialog()
                    dialog.set_message("请先选择正确的Excel文件!")
            else:
                dialog = SampleDialog()
                dialog.set_message("请先选择Excel文件,以及sheet表格!")
        elif click_id == "start_match":
            # 开始匹配
            try:
                self.__trans_threshold = int(self.et_trans_threshold.text())
                # 长度检查阈值的保存
                file = open(os.getcwd() + "/res/config.ini", "w")
                file.write("Threshold={0:d}".format(self.__trans_threshold))
                file.close()

                if len(self.__excel_select_col_1) > 0:
                    self.__select_dir_path_1 = self.et_dir_path_1.text()
                    print(u"select_uri: {0:s}".format(self.__select_dir_path_1))
                    # 给uri赋值成选择的uri
                    self.__select_dir_path_1 = self.et_dir_path_1.text()
                    # 给选择的基准列和对比列找出下标传入对比库
                    base_col_index = self.__list_col_data_2.index(self.__excel_select_col_base)
                    compare_col_index = []
                    for stri in self.__list_col_data_1:
                        if stri in self.__excel_select_col_1:
                            compare_col_index.append(self.__list_col_data_1.index(stri))
                    tc_tools = TC_Tools(self.__select_dir_path_1, select_sheet_1=self.et_sheet_1.text(),
                                        select_base_col=base_col_index,
                                        select_compare_col=compare_col_index,
                                        switch_check_list=self.__list_switch_check, trans_threshold=self.__trans_threshold,
                                        length_conf=self.__dict_length_conf)
                    self.logic.get_report_for_tc_tools(self.et_save_name.text(), tc_tools)
                    self.btn_match.setEnabled(False)
                    self.__start_dialog.set_message("正在进行翻译表检查,请稍后!!")
                    # self.__old_report_path = tc_tools.start_filter(self.et_save_name.text())
                    # dialog = SampleDialog()
                    # dialog.set_message("完成检查,详情请查看报告!")
                else:
                    dialog = SampleDialog()
                    dialog.set_message("请先选择好基本内容!!")
                    self.btn_match.setEnabled(True)
            except xlrd.biffh.XLRDError:
                dialog = SampleDialog()
                dialog.set_message("请将Excel文件的sheet重命名为英文格式!")
            except IOError as e:
                print(e)
                dialog = SampleDialog()
                dialog.set_message("请保证Excel文件所在路径中不包含中文!")
            except ValueError as e:
                print(e)
                dialog = SampleDialog()
                dialog.set_message("请先选择好基本内容!")

        elif click_id == "open_switch_check_list":
            """
            打开,需要检查的项的列表
            """
            self.__check_box.show()
        elif click_id == "open_report":
            """
            打开报告文件
            """
            self.__file_manager.open_excel(self.__old_report_path)
        elif click_id == "open_report_folder":
            """
              打开报告文件夹
            """
            if os.path.exists(os.getcwd() + "\\result"):
                self.__file_manager.open_folder(os.getcwd() + "\\result")
            else:
                dialog = SampleDialog()
                dialog.set_message("不存在文件夹!")
        elif click_id == "delete_logs":
            """
            删除日志文件
            """
            if os.path.exists(os.getcwd() + "/logs/match_error.txt"):
                self.__file_manager.delete_file(os.getcwd() + "/logs/match_error.txt")
        elif click_id == "open_compare_listview":
            """
            打开需要对比列的展示窗
            """
            self.__compare_listview.set_data(0, self.__excel_select_col_1)
            self.__compare_listview.show_listview()
        elif click_id == "":
            pass

    def get_selected_list_success(self, flag, list_item):
        """
        接口
        listview列表选择
        :param flag: 
        :param list_item: 
        :return:
        """
        self.__excel_select_col_1 = list_item
        print("compare_listview_callback:", end="")
        print(list_item)
        if len(list_item) == 0:
            self.btn_open_compare_list.setVisible(False)

    def get_list_data(self, flag, list_data):
        """
        接口
        得到选择器选择的
        :param flag:
        :param list_data:
        :return:
        """
        if len(list_data) > 0:
            if flag == self.__flag_1:
                # 需要处理的列
                print("compare_select_list_callback:", end="")
                print(list_data)
                if len(list_data) > 0:
                    self.__excel_select_col_1 = list_data
                    # 选择完这一列,显示隐藏的这个listview
                    self.btn_open_compare_list.setVisible(True)

            elif flag == self.__flag_2:
                # 基准的列
                print("base_select_callback:", end="")
                print(list_data)
                self.__excel_select_col_base = list_data[0]
                self.et_base_col.setText(list_data[0])
            elif flag == self.__sheet_flag_1:
                # 选择的sheet为
                self.__select_sheet_name = list_data[0]
                self.et_sheet_1.setText(self.__select_sheet_name)
                print("sheet_select_callback:", end="")
                print(self.__select_sheet_name)
                self.__select_sheet = self.__excel_data.sheet_by_name(self.__select_sheet_name)

        else:
            dialog = SampleDialog()
            dialog.set_message("请至少选择一项!")

    def __copy_excel_cache(self):
        """
        操作时先复制一份文件,防止出问题
        :return: 
        """
        uri_pos_1 = self.__select_dir_path_1.rfind(".")
        if self.__select_dir_path_1[uri_pos_1:].index("x") == 1:
            pos_1 = self.__select_dir_path_1.rfind("/")
            file_name_1 = self.__select_dir_path_1[pos_1 + 1:]
            if not os.path.exists(os.getcwd() + "/cache_data/" + file_name_1 + "x"):
                ExcelUtils.cvt_xls_to_xlsx(self.__select_dir_path_1,
                                           os.getcwd() + "/cache_data/" + file_name_1 + "x")
            self.__xlsx_uri_1 = os.getcwd() + "/cache_data/" + file_name_1 + "x"
        else:
            pos_1 = self.__select_dir_path_1.rfind("/")
            file_name_1 = self.__select_dir_path_1[pos_1 + 1:]
            if not os.path.exists(os.getcwd() + "/cache_data/" + file_name_1):
                FileUtils.copyFiles(self.__select_dir_path_1,
                                    os.getcwd() + "/cache_data/" + file_name_1)
            self.__xlsx_uri_1 = os.getcwd() + "/cache_data/" + file_name_1

    def get_custom_check_box(self, list_tuple, sender):
        """
        checkbox 的选择内容接口回调
        :param list_tuple: 
        :param sender: 
        :return: 
        """
        if sender == self.__check_box:
            list_value = []
            self.__list_switch_check = []
            for index in list_tuple:
                list_value.append(self.__list_check_data[index])
            for item in self.__dict_check_switch.items():
                if item[1][0] in list_value:
                    self.__list_switch_check.append(int(item[0]))
                    item[1][1] = True
                else:
                    item[1][1] = False

            print("选择的需要检查项的下标为:", end="")
            print(self.__list_switch_check)
            # 控制阈值显示框
            if 9 in self.__list_switch_check:
                self.et_trans_threshold.setVisible(True)
                self.lab_trans_threshold.setVisible(True)
            else:
                self.et_trans_threshold.setVisible(False)
                self.lab_trans_threshold.setVisible(False)
            # 控制配置表选择Frame的显示
            if 11 in self.__list_switch_check:
                self.frame_select_length_conf.setVisible(True)
            else:
                self.frame_select_length_conf.setVisible(False)

            file = open(os.getcwd() + "/res/default_checked.json", "w+")
            json.dump(self.__dict_check_switch, file)
            file.close()

    def get_drag_file_uri(self, parent, file_uri):
        pos = file_uri.rfind(".")
        suffix_name = file_uri[pos + 1:]
        print(suffix_name)
        suffix_name = suffix_name.upper()
        if parent == self.frame_select_excel and (suffix_name == "XLS" or suffix_name == "XLSX"):
            self.__select_dir_path_1 = file_uri
            self.et_dir_path_1.setText(file_uri)
            print(file_uri)
            if len(self.__select_dir_path_1) > 0:
                self.et_dir_path_1.setText(self.__select_dir_path_1)
                self.__list_col_data_1 = []
                # 选择了新的地址以后就隐藏掉它
                self.btn_open_compare_list.setVisible(False)
                # 选择完excel后,读取所有sheet表格到list
                self.__excel_data = xlrd.open_workbook(self.__select_dir_path_1)
                self.__list_sheet = self.__excel_data.sheet_names()  # 返回所有sheet的列表
                # 清空各种数据
                self.__list_sheet_data_1 = self.__list_sheet
                self.__list_col_data_1 = []
                self.__list_col_data_2 = []
                self.__excel_select_col_1 = []
                self.__excel_select_col_base = 0
                self.__old_report_path = ""
                if self.__list_sheet is not None and len(self.__list_sheet) > 0:
                    self.__select_sheet_name = self.__list_sheet[0]
                    self.et_sheet_1.setText(self.__list_sheet[0])
                    self.__select_sheet = self.__excel_data.sheet_by_name(self.__select_sheet_name)
                self.et_base_col.setText("")

            else:
                self.__select_dir_path_1 = self.et_dir_path_1.text()
        elif parent == self.frame_select_length_conf and (suffix_name == "XLS" or suffix_name == "XLSX"):
            self.__dict_uri_conf["excel_length_conf"] = file_uri
            if os.path.exists(os.getcwd() + "/res/uri_conf.json"):
                file = open(os.getcwd() + "/res/uri_conf.json", "w+")
                try:
                    json.dump(self.__dict_uri_conf, file)
                except Exception as e:
                    print(e)
                finally:
                    file.close()
            if len(self.__dict_uri_conf["excel_length_conf"]) > 0:
                self.et_trans_length_conf.setText(self.__dict_uri_conf["excel_length_conf"])
                # 选择完excel后,读取所有sheet表格到list
                excel_length_conf_data = xlrd.open_workbook(self.__dict_uri_conf["excel_length_conf"])
                sheet = excel_length_conf_data.sheet_by_index(0)  # 返回所有sheet的列表
                list_col_1 = sheet.col_values(0)
                list_col_2 = sheet.col_values(1)
                self.__dict_length_conf["Key"] = list_col_1
                self.__dict_length_conf["Length"] = list_col_2
            print("拖拽选择的长度检查配置地址:{uri_conf}".format(uri_conf=self.__dict_uri_conf))

    def on_message_receive(self, sender, mst_id, args):
        """
        实现观察者模式的消息监听
        :param sender: 
        :param mst_id: 
        :param args: 
        :return: 
        """
        if sender == self.logic:
            if mst_id == TCTBaseLogic.success_report_finished:
                # print(args[0])
                # dialog = SampleDialog()
                # dialog.set_message("测试回调弹窗!")
                self.__old_report_path = args[0]
                self.__start_dialog.close()
                self.__run_dialog.close()
                dialog = SampleDialog()
                dialog.set_message("完成检查,详情请查看报告!")
                self.btn_match.setEnabled(True)
            if mst_id == TCTBaseLogic.success_progress:
                # print(args)
                self.__start_dialog.close()
                self.__run_dialog.set_message("正在检查翻译表中,请稍后!\n已完成:{0:d}%/{1:d}%".format(args[0], args[1]))

    @staticmethod
    def main():
        """
        window主函数
        """

        # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
        app = QApplication(sys.argv)
        # pyqt的QMainwWindow类的实体
        window = TCTMainActivity()
        # resize()方法调整窗口的大小。(宽,高)
        window.resize(1000, 750)
        # move()方法移动窗口在屏幕上的位置到(x,y)坐标。
        window.move(450, 200)
        # 设置窗口最大的大小 (宽,高)
        # window.setFixedSize(1280, 720)
        # 从布局文件中加载ui界面
        # loadUi('./res/main_activity.ui', window)
        # 设置窗口的标题
        window.setWindowTitle("翻译表检查工具")
        # 设置窗口的图标，引用当前目录下的web.png图片
        window.setWindowIcon(QIcon('./res/tc_icon.png'))
        # 窗口显示
        window.show()
        # 系统exit()方法确保应用程序干净的退出
        # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
        sys.exit(app.exec_())

