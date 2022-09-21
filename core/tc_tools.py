# encoding=utf-8
import os

import xlrd
import xlwt
from xlwt import Borders

from BaseLibrary.common_utils.stringutils import StringUtils

"""
@author: v_jjyjiang 
@Description: TODO(这里用一句话描述这个模块的作用)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: tc_tools.py
"""


class TC_Tools(object):
    def __init__(self, xls_uri_1, select_sheet_1="", select_base_col=0,
                 select_compare_col=None):
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
        self.__list_report_data = []

        if not (os.path.exists(os.getcwd() + "/cache_data")):
            os.makedirs(os.getcwd() + "/cache_data")
        if not (os.path.exists(os.getcwd() + "/result")):
            os.makedirs(os.getcwd() + "/result")

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
        # 集合的[2]为报错内容
        self.__list_report_data = []

        # 存放基准列的数据集合
        self.__list_base = sheet_1.col_values(self.__select_base_col)

        # 通过循环需要对比列的下标,来获得对比列的集合,然后和基准列做对比
        for col_index_compare in self.__select_compare_col:
            # print col_index_compare
            # print len(list_compare)
            list_compare = sheet_1.col_values(col_index_compare)
            index = 1
            while index < len(self.__list_base):
                # print "base: %s  ---- compare: %s" % (list_base[index], list_compare[index])
                base_string = self.__list_base[index]
                compare_string = list_compare[index]
                # 检查这个是不是空的...
                if not StringUtils.string_is_no_empty(compare_string):
                    self.__list_report_data.append([(index, col_index_compare),
                                                    compare_string, "存在漏翻"])
                    # print "存在漏翻 (%d,%d)" % (index + 1, col_index_compare + 1)

                # 检查成对出现的标点符号
                elif not StringUtils.check_strings_twin_mark(compare_string):
                    self.__list_report_data.append([(index, col_index_compare),
                                                    compare_string,
                                                    "标点符号问题,本应成对存在的标点符号,少了一个"])
                    # print "标点问题 (%d,%d)" % (index + 1, col_index_compare + 1)

                # # 检查占位符后面后面的标记是否被空格隔开
                # elif not StringUtils.check_string_placeholder(compare_string):
                #     self.__list_report_data.append([(index, col_index_compare),
                #                                                   compare_string,
                #                                                   "占位符后的标记是否被空格隔开"])
                #    #print "占位符问题(%d,%d)" % (index + 1, col_index_compare + 1)

                # 检查需要对比的列中字符串里出现的占位符和基准列中是否相同
                elif not StringUtils.compare_strings_placeholder(base_string, compare_string):
                    self.__list_report_data.append([(index, col_index_compare),
                                                    compare_string,
                                                    "占位符问题(%),译文中的%后的标记与基准列的不一致"])
                    # print "占位符对比问题(%d,%d)" % (index + 1, col_index_compare + 1)
                    # 检查需要对比的列中字符串里出现的转义字符和基准列中是否相同
                    # elif not StringUtils.compare_strings_escape(base_string, compare_string):
                    #     self.__list_report_data.append([(index, col_index_compare),
                    #                                                   compare_string,
                    #                                                   "转义字符问题,译文中的转义字符如换行等,与基准列可能存在数量,和内容上的不同"])
                    # print "转义字符问题问题(%d,%d)" % (index + 1, col_index_compare + 1)

                    # 检查需要对比的列中字符串里出现的数字字符和基准列中是否相同
                    # elif not StringUtils.compare_strings_num(base_string, compare_string):
                    #     self.__list_report_data.append([(index, col_index_compare),
                    #                                                   compare_string,
                    #                                                   "数字不匹配,译文中的的数字,与基准列存在不同"])
                    # print "数字问题(%d,%d)" % (index + 1, col_index_compare + 1)

                # 检查是否句中出现两个空格
                # elif not StringUtils.check_strings_multi_blank(compare_string):
                #     print "空格问题(%d,%d)" % (index+1, col_index_compare+1)
                #     pass
                index += 1
        print("report_num: %d" % len(self.__list_report_data))
        # for data in self.__list_report_data:
        #     for stri in data:
        #         print "value: " + str(stri),
        #     print ""
        # 把数据输出成excel文档
        report_uri = self.create_result(file_name, self.__list_base,
                                        self.__list_report_data)

        return report_uri

    def create_result(self, file_name, list_data, list_data_2):
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

        excel = xlwt.Workbook(encoding="utf-8")
        style = xlwt.XFStyle()
        font0 = xlwt.Font()
        font0.name = u"宋体"
        font0.bold = True
        style.font = font0

        style1 = xlwt.XFStyle()
        font1 = xlwt.Font()
        font1.colour_index = 2
        font1.name = u"宋体"
        font1.bold = True
        style1.font = font1

        style2 = xlwt.XFStyle()
        font2 = xlwt.Font()
        font2.colour_index = 4
        font2.name = u"宋体"
        font2.bold = True
        style2.font = font2

        style3 = xlwt.XFStyle()
        for i in range(2, 0x53):                # 设置单元格下框线样式
            borders = Borders()
            borders.left = i
            borders.right = i
            borders.top = i
            borders.bottom = i
            style3.borders = borders         #将赋值好的模式参数导入Style
        font3 = xlwt.Font()
        font3.colour_index = 2
        font3.name = u"宋体"
        font3.bold = True
        style3.font = font3


        # 报告sheet表格的处理  (总表)
        sheet = excel.add_sheet('data', cell_overwrite_ok=True)
        f_col_1 = sheet.col(0)
        f_col_1.width = 1000 * 20

        f_row_num = 0
        for data in list_data_2:
            f_col_num = 0
            # +2表示给报告的第一列加上Key,第二列加上基准列,以及最后一列加上报错内容
            while f_col_num < len(self.__select_compare_col) + 3:
                # 第一行的标签额外写
                if f_row_num == 0:
                    if f_col_num == 0:
                        sheet.write(f_row_num, f_col_num, "报错内容", style2)
                    elif f_col_num == 1:
                        # 待定需要记录一个key的位置(列) #TODO
                        sheet.write(f_row_num, f_col_num, sheet_data.cell(0, 0).value, style2)
                    elif f_col_num == 2:
                        # 基准列的标签
                        sheet.write(f_row_num, f_col_num,
                                    sheet_data.cell(0, self.__select_base_col).value, style2)
                    else:
                        # 其他列的标签
                        sheet.write(f_row_num, f_col_num,
                                    sheet_data.cell(0,
                                                    self.__select_compare_col[f_col_num - 3]).value,
                                    style2)
                else:
                    if f_col_num == 0:
                        # 报错内容
                        sheet.write(f_row_num, f_col_num, data[2], style1)
                    elif f_col_num == 1:
                        # key
                        sheet.write(f_row_num, f_col_num, sheet_data.cell(data[0][0], 0).value,
                                    style)
                    elif f_col_num == 2:
                        # 基准列
                        sheet.write(f_row_num, f_col_num,
                                    sheet_data.cell(data[0][0], self.__select_base_col).value,
                                    style)
                    else:
                        # 其他列
                        if (data[0][0], self.__select_compare_col[f_col_num - 3]) == data[0]:
                            sheet.write(f_row_num, f_col_num,
                                        sheet_data.cell(data[0][0], self.__select_compare_col[
                                            f_col_num - 3]).value, style1)
                        else:
                            sheet.write(f_row_num, f_col_num,
                                        sheet_data.cell(data[0][0], self.__select_compare_col[
                                            f_col_num - 3]).value, style)

                f_col_num += 1
            f_row_num += 1

        excel.save(self.__result_data_uri)
        print(self.__result_data_uri)
        return self.__result_data_uri


if __name__ == '__main__':
    # ct_tools = TC_Tools("F://quest.xls", "F://AllTranslations(1).xls", select_col=26,
    #                     select_sheet_2="Main Sheet")
    # ct_tools.start_filter(123)
    pass
