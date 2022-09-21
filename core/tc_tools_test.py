# encoding=utf-8
import os
from abc import abstractmethod

import xlrd
import xlwt
from xlwt import Borders, Pattern

from BaseLibrary.common_utils.stringutils import StringUtils

"""
@author: v_jjyjiang 
@Description: TODO(这里用一句话描述这个模块的作用)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: tc_tools.py

目前能检查的项:
1."开启漏翻检查"
2."开启标点符号检查,半角/全角是否一致或数量不一致等"
3."开启占位符问题(%),译文中的%后的标记与基准列的是否一致"
4."存在标签检查,暂时只有'{}'标签"
5."开启转义字符检查,包括其数量和一致性,如:'\\n',建议按需选择,减少误报"
6."开启html/xml中标签Name检查,如:<xxxx><yyyy/>"
7."开启颜色十六进制标签的检查,包括数量和一致性,如:[ffffff]"
8."开启阿拉伯数字的检查,包括数量和一致性,如1, 100, 1000"
9."开启检查英文中是否包含中文检查"
10."开启译文长度的检查(与基准参照文的阈值来比较)"

"""


class TC_Tools(object):
    def __init__(self, xls_uri_1, select_sheet_1="", select_base_col=0,
                 select_compare_col=None, switch_check_list=[], trans_threshold=100, length_conf={"Key": [], "Length": []}):
        """
        :param xls_uri_1: 检查的excel的地址
        :param select_sheet_1: 选择的sheet
        :param select_base_col: 基准列
        :param select_compare_col: 需要对比的列
        :param switch_check_list: 这个list的value需要做一个说明
        0存在,表示开启漏翻检查
        1存在,开启标点符号检查,半角/全角是否一致或数量不一致等
        2存在,表示开启占位符问题(%),译文中的%后的标记与基准列的是否一致
        3存在,表示开启标签检查,暂时只有'{}'标签
        4存在,表示开启转义字符检查,包括其数量和一致性,如:'\\n',建议按需选择,减少误报
        5存在,表示开启html/xml中标签Name检查,如:<xxxx><yyyy/>
        6存在,表示开启颜色十六进制标签的检查,包括数量和一致性,如:[ffffff]
        7存在,表示开启阿拉伯数字的检查,包括数量和一致性,如1, 100, 1000
        8存在,表示开启检查英文中是否包含中文检查
        9存在,表示开启译文长度的检查(与基准参照文的阈值来比较) 
        10存在,表示开启Key和文本头尾有空格或换行的检查
        :param trans_threshold 长度检查的阈值
        """

        self.__result_name_num = 0
        # 传入的excel文件地址
        self.__xls_uri_1 = xls_uri_1
        # 文件复制/转化后的地址
        self.__xlsx_uri_1 = ""
        # 选择的需要处理的sheet
        self.__select_sheet_1 = select_sheet_1
        # 选择的作为基准的列
        self.__select_base_col = select_base_col
        # 选择的需要比对的列的集合
        self.__select_compare_col = select_compare_col
        # 第一个xls获取到的数据集
        self.__list_data_1 = []
        # 存放基准列的数据集合
        self.__list_base = []
        # 报告字典
        self.__list_report_data = {}
        # 检查项的开关list
        self.__list_switch = switch_check_list
        # 需要检查的语言
        self.__list_language_switch = ["EN", "EN-US", "EN-CA", "EN-UK"]
        # 检查译文长度的阈值
        self.__trans_threshold = trans_threshold
        # 进度监听
        self.__progress_listener = None
        # 读取AOV检查指定字节长度配置文件后的配置数据
        self.__dit_length_conf = length_conf

        print("选择的开关:", end="")
        print(self.__list_switch)

        print("Threshold:", end="")
        print(self.__trans_threshold)

        if not (os.path.exists(os.getcwd() + "/cache_data")):
            os.makedirs(os.getcwd() + "/cache_data")
        if not (os.path.exists(os.getcwd() + "/result")):
            os.makedirs(os.getcwd() + "/result")

    def set_progress_listener(self, listener):
        self.__progress_listener = listener

    def start_filter(self, file_name):
        # 运行时清空上次的数据
        self.__list_data_1 = []
        self.__xlsx_uri_1 = ""
        self.__result_name_num = 0
        # uri_pos_1 = self.__xls_uri_1.rfind(".")
        # if self.__xls_uri_1[uri_pos_1:].index("x") == 1:
        #     pos_1 = self.__xls_uri_1.rfind("/")
        #     file_name_1 = self.__xls_uri_1[pos_1 + 1:]
        #     if not os.path.exists(os.getcwd() + "/cache_data/" + file_name_1 + "x"):
        #         ExcelUtils.cvt_xls_to_xlsx(self.__xls_uri_1,
        #                                    os.getcwd() + "/cache_data/" + file_name_1 + "x")
        #     self.__xlsx_uri_1 = os.getcwd() + "/cache_data/" + file_name_1 + "x"
        # else:
        #     pos_1 = self.__xls_uri_1.rfind("/")
        #     file_name_1 = self.__xls_uri_1[pos_1 + 1:]
        #     if not os.path.exists(os.getcwd() + "/cache_data/" + file_name_1):
        #         FileUtils.copyFiles(self.__xls_uri_1, os.getcwd() + "/cache_data/" + file_name_1)
        #     self.__xlsx_uri_1 = os.getcwd() + "/cache_data/" + file_name_1

        # xls里的数据获取
        data_1 = xlrd.open_workbook(self.__xls_uri_1)
        sheet_1 = data_1.sheet_by_name(self.__select_sheet_1)

        # 选择的作为基准的列
        print("select_base_col: {0:d}".format(self.__select_base_col))
        # 选择的需要比对的列的集合
        print("select_compare_list_col:", end="")
        print(self.__select_compare_col)

        # sheet_1_row_num = sheet_1.nrows
        # print("sheet_row_num: {0:d}".format(sheet_1_row_num))

        # i = 1
        # while i <= sheet_1_row_num:
        #     data_temp = sheet_1.cell(row=i, column=self.__select_col).value
        #     data_temp = str(data_temp)
        #     pos_2 = data_temp.rfind(".")
        #     data_temp = data_temp[0:pos_2]
        #     self.__list_data_1.append(str(data_temp))
        #     i += 1
        # 用compare_col做key, value为1个集合, 集合的[0]为在原excel中的单元格的坐标用数组来存, 集合的[1]为原excel中当前单元格的内容,
        # 集合的[2]为报错内容   [(index, col_index_compare),compare_string, "xxx"]

        # 存放基准列的数据集合
        self.__list_base = sheet_1.col_values(self.__select_base_col)
        # print("Base_Col_Num: {0:d}".format(len(self.__list_base)))
        # print(self.__list_base)
        # for i in self.__list_base:
        #     if i is "您确定要开始新游戏吗?\\n之后您还可以通过FB或GP账号登录，载入当前游戏数据。":
        #         print(11111111111111111111111111111111111)
        # 废弃, 在判断条件里添加key存在的判断方式
        # count = 0
        # while count < len(self.__list_base):
        #     self.__list_report_data[count] = []  # 之后在 append 各个列对应的报错内容
        #     count += 1
        self.__list_report_data[0] = []  # 添加这个,防止在生成报告时,由于第一行是预留的,导致报告内容会少了第一个
        base_length = len(self.__list_base)
        for index in range(base_length):
            # 新增检查Key 是否为空
            if StringUtils.string_is_no_empty(sheet_1.cell(index,
                                                           0).value) is False:
                if index not in self.__list_report_data.keys():
                    self.__list_report_data[index] = []
                ipErrorInfo = IPReportDetails()
                ipErrorInfo.col = index
                ipErrorInfo.content_string = ""
                ipErrorInfo.error_info = "此条翻译Key为空".format(sheet_1.cell(index, 0).value)
                self.__list_report_data[index].append(ipErrorInfo)

            if (10 in self.__list_switch) and (
                        StringUtils.check_string_head_ending(sheet_1.cell(index,
                                                                          0).value) is False):
                if index not in self.__list_report_data.keys():
                    self.__list_report_data[index] = []
                ipErrorInfo = IPReportDetails()
                ipErrorInfo.col = index
                ipErrorInfo.content_string = ""
                ipErrorInfo.error_info = "此条翻译Key中包含空格或换行".format(sheet_1.cell(index, 0).value)
                self.__list_report_data[index].append(ipErrorInfo)

        progress_list = []
        for percent in range(0, 100, 5):
            progress_list.append(percent)
        progress_stop = 0
        progress_num = 0

        # 通过循环需要对比列的下标,来获得对比列的集合,然后和基准列做对比
        for index_parent in range(len(self.__select_compare_col)):
            col_index_compare = self.__select_compare_col[index_parent]
            # print col_index_compare
            # print len(list_compare)
            list_compare = sheet_1.col_values(col_index_compare)
            # print(list_compare)
            # print("list_base_0 :{0:s}".format(self.__list_base[0]))
            # print("list_compare_0 :{0:s}".format(list_compare[0]))
            index = 0

            while index < base_length:
                try:
                    # 进度返回, (total_num,current_num)
                    progress_num += 1
                    progress = int((progress_num / (base_length * len(self.__select_compare_col))) * 100)
                    # print(progress)
                    if (progress in progress_list) and progress > progress_stop:
                        progress_stop = progress
                        self.__progress_listener.get_progress_data(self, (progress, 100))
                except Exception as e:
                    print(e)
                    print("单独跑脚本无需实现进度接口,会捕获这个异常")

                # print "base: %s  ---- compare: %s" % (list_base[index], list_compare[index])
                base_string = self.__list_base[index]
                compare_string = list_compare[index]
                language_head = sheet_1.cell(0, col_index_compare).value
                if index > 0:
                    # 检查这个是不是空的...
                    if StringUtils.string_is_no_empty(compare_string) is False:
                        if index not in self.__list_report_data.keys():
                            self.__list_report_data[index] = []
                        if 0 in self.__list_switch:
                            ipErrorInfo = IPReportDetails()
                            ipErrorInfo.col = col_index_compare
                            ipErrorInfo.content_string = compare_string
                            ipErrorInfo.error_info = "{0:s}:存在漏翻".format(language_head)
                            self.__list_report_data[index].append(ipErrorInfo)
                    elif StringUtils.check_string_exist_blacklist(compare_string)[0] is False:
                        error_code = StringUtils.check_string_exist_blacklist(compare_string)[1]
                        if index not in self.__list_report_data.keys():
                            self.__list_report_data[index] = []
                        ipErrorInfo = IPReportDetails()
                        ipErrorInfo.col = col_index_compare
                        ipErrorInfo.content_string = compare_string
                        ipErrorInfo.error_info = "{0:s}:存在Excel内置报错内容: \"{1:s}\"".format(language_head,
                                                                                         xlrd.error_text_from_code[error_code])
                        self.__list_report_data[index].append(ipErrorInfo)

                    else:  # 检查成对出现的标点符号
                        if (1 in self.__list_switch) and (
                                    StringUtils.check_strings_twin_mark(compare_string) is False):
                            if index not in self.__list_report_data.keys():
                                self.__list_report_data[index] = []
                            ipErrorInfo = IPReportDetails()
                            ipErrorInfo.col = col_index_compare
                            ipErrorInfo.content_string = compare_string
                            ipErrorInfo.error_info = "{0:s}:标点符号问题,半角/全角不一致或数量不一致".format(language_head)
                            self.__list_report_data[index].append(ipErrorInfo)
                            # print "标点问题 (%d,%d)" % (index + 1, col_index_compare + 1)

                        # 检查需要对比的列中字符串里出现的占位符和基准列中是否相同
                        if (2 in self.__list_switch) and (
                                    StringUtils.compare_strings_placeholder(base_string, compare_string) is False):
                            if index not in self.__list_report_data.keys():
                                self.__list_report_data[index] = []
                            ipErrorInfo = IPReportDetails()
                            ipErrorInfo.col = col_index_compare
                            ipErrorInfo.content_string = compare_string
                            ipErrorInfo.error_info = "{0:s}:占位符问题(%),译文中的%后的标记与基准列的不一致".format(language_head)
                            self.__list_report_data[index].append(ipErrorInfo)
                        if (3 in self.__list_switch) and (
                                    StringUtils.compare_strings_sign_inner(base_string, compare_string) is False):
                            if index not in self.__list_report_data.keys():
                                self.__list_report_data[index] = []
                            ipErrorInfo = IPReportDetails()
                            ipErrorInfo.col = col_index_compare
                            ipErrorInfo.content_string = compare_string
                            ipErrorInfo.error_info = "{0:s}:存在标签中的内容或数量不一致".format(language_head)
                            self.__list_report_data[index].append(ipErrorInfo)

                        # 检查需要对比的列中字符串里出现的转义字符和基准列中是否相同
                        if (4 in self.__list_switch) and (
                                    StringUtils.compare_strings_escape(base_string,
                                                                       compare_string) is False):
                            if index not in self.__list_report_data.keys():
                                self.__list_report_data[index] = []
                            ipErrorInfo = IPReportDetails()
                            ipErrorInfo.col = col_index_compare
                            ipErrorInfo.content_string = compare_string
                            ipErrorInfo.error_info = "{0:s}:转义字符问题,译文中的转义字符如换行(\\n)等".format(language_head)
                            self.__list_report_data[index].append(ipErrorInfo)
                            # print ("转义字符问题问题(%d,%d)" % (index + 1, col_index_compare + 1))

                        # 检查需要对比的列中字符串里出现的html/xml所用标签Name,如:<xxxx><yyyy/>
                        if (5 in self.__list_switch) and (
                                    StringUtils.compare_strings_label_content(base_string,
                                                                              compare_string) is False):
                            if index not in self.__list_report_data.keys():
                                self.__list_report_data[index] = []
                            ipErrorInfo = IPReportDetails()
                            ipErrorInfo.col = col_index_compare
                            ipErrorInfo.content_string = compare_string
                            ipErrorInfo.error_info = "{0:s}:html/xml标签问题,译文中的标签存在不一致".format(language_head)
                            self.__list_report_data[index].append(ipErrorInfo)

                        # 检查需要对比的列中字符串里出现颜色十六进制标签的检查,包括数量和一致性,如:[ffffff]
                        if (6 in self.__list_switch) and (
                                    StringUtils.compare_strings_brackets_content(base_string,
                                                                                 compare_string) is False):
                            if index not in self.__list_report_data.keys():
                                self.__list_report_data[index] = []
                            ipErrorInfo = IPReportDetails()
                            ipErrorInfo.col = col_index_compare
                            ipErrorInfo.content_string = compare_string
                            ipErrorInfo.error_info = "{0:s}:颜色标签[xxxxxx],译文中的标签存在不一致".format(language_head)
                            self.__list_report_data[index].append(ipErrorInfo)

                        # 检查需要对比的列中字符串里出现阿拉伯数字的检查,包括数量和一致性,如1, 100, 1000
                        if (7 in self.__list_switch) and (
                                    StringUtils.compare_strings_num(base_string,
                                                                    compare_string) is False):
                            if index not in self.__list_report_data.keys():
                                self.__list_report_data[index] = []
                            ipErrorInfo = IPReportDetails()
                            ipErrorInfo.col = col_index_compare
                            ipErrorInfo.content_string = compare_string
                            ipErrorInfo.error_info = "{0:s}:阿拉伯数字,译文中的数字存在不一致".format(language_head)
                            self.__list_report_data[index].append(ipErrorInfo)

                        # 检查英文中是否包含中文字符
                        try:
                            if (8 in self.__list_switch) and ((str(language_head)).upper() in self.__list_language_switch) and (
                                        StringUtils.check_en_string_exist_cn(compare_string) is False):
                                if index not in self.__list_report_data.keys():
                                    self.__list_report_data[index] = []
                                ipErrorInfo = IPReportDetails()
                                ipErrorInfo.col = col_index_compare
                                ipErrorInfo.content_string = compare_string
                                ipErrorInfo.error_info = "{0:s}:英文翻译中包含中文".format(language_head)
                                self.__list_report_data[index].append(ipErrorInfo)

                        except Exception as e:
                            print(e)

                            # 检查译文长度
                        if (9 in self.__list_switch) and (
                                    StringUtils.compare_strings_length(base_string, compare_string, self.__trans_threshold) is False):
                            if index not in self.__list_report_data.keys():
                                self.__list_report_data[index] = []
                            ipErrorInfo = IPReportDetails()
                            ipErrorInfo.col = col_index_compare
                            ipErrorInfo.content_string = compare_string
                            ipErrorInfo.error_info = "{0:s}:译文长度相对原文长度的比值大于指定的阈值".format(language_head)
                            self.__list_report_data[index].append(ipErrorInfo)

                            # 检查文本头尾是否有空格
                        if (10 in self.__list_switch) and (
                                    StringUtils.check_string_head_ending(compare_string) is False):
                            if index not in self.__list_report_data.keys():
                                self.__list_report_data[index] = []
                            ipErrorInfo = IPReportDetails()
                            ipErrorInfo.col = col_index_compare
                            ipErrorInfo.content_string = compare_string
                            ipErrorInfo.error_info = "{0:s}:文本头尾有空格或换行".format(language_head)
                            self.__list_report_data[index].append(ipErrorInfo)

                        try:
                            # AOV根据配置检查指定Key对应的翻译长度
                            if 11 in self.__list_switch:
                                keys = self.__dit_length_conf["Key"]
                                lengths = self.__dit_length_conf["Length"]
                                for i in range(len(keys)):
                                    key = keys[i]
                                    length = int(lengths[i])
                                    # print(key)
                                    # print(length)
                                    if key in sheet_1.cell(index, 0).value:
                                        result = StringUtils.check_utf_bytes_length(compare_string, length)
                                        if result[0] is False:
                                            if index not in self.__list_report_data.keys():
                                                self.__list_report_data[index] = []
                                            ipErrorInfo = IPReportDetails()
                                            ipErrorInfo.col = col_index_compare
                                            ipErrorInfo.content_string = compare_string
                                            ipErrorInfo.error_info = "{0:s}:该Key进行了文本长度配置检查,该文本超过配置中指定长度:{1:d}\t 当前长度:{2:d}".format(
                                                language_head, length, result[1])
                                            self.__list_report_data[index].append(ipErrorInfo)
                        except Exception as e:
                            print(e)
                index += 1

        # 废弃, 在判断条件里添加key存在的判断方式
        # delete_key = []
        # for data in self.__list_report_data.items():
        #     if len(data[1]) == 0:
        #         delete_key.append(data[0])
        # for key in delete_key:
        #     self.__list_report_data.pop(key)

        print("report_num: %d" % len(self.__list_report_data))
        # 把数据输出成excel文档
        report_uri = self.create_result(file_name, self.__list_report_data)

        return report_uri

    def create_result(self, file_name, dict_data):
        # 生成报告
        while True:
            if os.path.exists(os.getcwd() + "//result//%s_%d.xls" % (
                    file_name, self.__result_name_num)):
                self.__result_name_num += 1
            if not os.path.exists(os.getcwd() + "//result//%s_%d.xls" % (
                    file_name, self.__result_name_num)):
                break
        self.__result_data_uri = os.getcwd() + "//result//%s_%d.xls" % (
            file_name, self.__result_name_num)

        # xls里的数据获取
        excel_data = xlrd.open_workbook(self.__xls_uri_1)
        sheet_data = excel_data.sheet_by_name(self.__select_sheet_1)

        # -----样式设置----------------
        excel = xlwt.Workbook(encoding="utf-8")
        alignment = xlwt.Alignment()  # 创建居中
        alignment.horz = xlwt.Alignment.HORZ_LEFT  # 可取值: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
        alignment.vert = xlwt.Alignment.VERT_CENTER  # 可取值: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT  # 自动换行

        style = xlwt.XFStyle()
        style.alignment = alignment  # 给样式添加文字居中属性
        font0 = xlwt.Font()
        font0.name = u"宋体"
        font0.bold = True
        style.font = font0

        style1 = xlwt.XFStyle()
        style1.alignment = alignment  # 给样式添加文字居中属性
        font1 = xlwt.Font()
        font1.colour_index = 2
        font1.name = u"宋体"
        font1.bold = True
        style1.font = font1

        style2 = xlwt.XFStyle()
        style2.alignment = alignment  # 给样式添加文字居中属性
        font2 = xlwt.Font()
        font2.colour_index = 4
        font2.name = u"宋体"
        font2.bold = True
        style2.font = font2

        style3 = xlwt.XFStyle()
        style3.alignment = alignment  # 给样式添加文字居中属性
        borders = Borders()
        borders.left = 2
        borders.right = 2
        borders.top = 2
        borders.bottom = 2
        style3.borders = borders  # 将赋值好的模式参数导入Style
        pattern = Pattern()  # 创建一个模式
        pattern.pattern = Pattern.SOLID_PATTERN  # 设置其模式为实型
        pattern.pattern_fore_colour = 27
        style3.pattern = pattern  # 将赋值好的模式参数导入Style
        font3 = xlwt.Font()
        font3.colour_index = 2
        font3.name = u"宋体"
        font3.bold = True
        style3.font = font3

        # 报告sheet表格的处理  (总表)
        sheet = excel.add_sheet('data', cell_overwrite_ok=True)
        f_col_0 = sheet.col(0)
        f_col_0.set_width(700 * 20)
        f_col_1 = sheet.col(1)
        f_col_1.set_width(600 * 20)

        f_col_num = 2
        while f_col_num < len(self.__select_compare_col) + 3:
            f_col = sheet.col(f_col_num)
            f_col.set_width(400 * 20)
            f_col_num += 1

        # 先写好报告第一行的内容
        first_col_num = 0
        # +3表示给报告的第一列加上Key,第二列加上基准列,以及最后一列加上报错内容
        while first_col_num < len(self.__select_compare_col) + 3:
            # 第一行的标签额外写
            if first_col_num == 0:
                sheet.write(0, first_col_num, "报错内容", style2)
            elif first_col_num == 1:
                # 待定需要记录一个key的位置(列) #TODO
                sheet.write(0, first_col_num, sheet_data.cell(0, 0).value, style2)
            elif first_col_num == 2:
                # 基准列的标签
                sheet.write(0, first_col_num, sheet_data.cell(0, self.__select_base_col).value,
                            style2)
            else:
                # 其他列的标签
                sheet.write(0, first_col_num,
                            sheet_data.cell(0,
                                            self.__select_compare_col[first_col_num - 3]).value,
                            style2)
            first_col_num += 1

        # 写报告内容
        f_row_num = 0
        for items_data in dict_data.items():  # 这样写,由于第一行要写标签,导致会漏掉一个,所以,我在字典的第一项加了个空的值
            compare_row = items_data[0]
            compare_content = items_data[1]
            f_col_num = 0
            # +3表示给报告的第一列加上Key,第二列加上基准列,以及最后一列加上报错内容
            while f_col_num < len(self.__select_compare_col) + 3:
                # 第一行的标签额外写
                if f_row_num > 0:
                    if f_col_num == 0:
                        # 报错内容
                        ex_data = []
                        for content in compare_content:
                            ex_data.append(content.error_info)
                        ex_str = "\n".join(ex_data)
                        sheet.write(f_row_num, f_col_num, ex_str, style1)
                    elif f_col_num == 1:
                        # key
                        sheet.write(f_row_num, f_col_num,
                                    sheet_data.cell(compare_row, 0).value,
                                    style)
                    elif f_col_num == 2:
                        # 基准列
                        sheet.write(f_row_num, f_col_num,
                                    sheet_data.cell(compare_row, self.__select_base_col).value,
                                    style)
                    else:
                        # 其他列
                        sheet.write(f_row_num, f_col_num,
                                    sheet_data.cell(compare_row, self.__select_compare_col[
                                        f_col_num - 3]).value, style)
                # 有问题的其他列标红
                for col_content in compare_content:
                    # 第一行的标签额外写
                    if f_row_num > 0 and f_col_num > 2:
                        if self.__select_compare_col[f_col_num - 3] == col_content.col:
                            sheet.write(f_row_num, f_col_num,
                                        sheet_data.cell(compare_row, col_content.col).value, style3)
                f_col_num += 1
            f_row_num += 1

        excel.save(self.__result_data_uri)
        print(self.__result_data_uri)
        return self.__result_data_uri


class IPReportDetails(object):
    col = -1
    content_string = ""
    error_info = ""
    # 报错文本的位置信息
    error_position = []


class TCTProgressListener(object):
    @abstractmethod
    def get_progress_data(self, parent, progress_data):
        print("请实现未实现的方法")
        raise NotImplementedError


if __name__ == '__main__':
    # ct_tools = TC_Tools("F://quest.xls", "F://AllTranslations(1).xls", select_col=26,
    #                     select_sheet_2="Main Sheet")
    # ct_tools.start_filter(123)
    print(xlrd.error_text_from_code)
    pass
