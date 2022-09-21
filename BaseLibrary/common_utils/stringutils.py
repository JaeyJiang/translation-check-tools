# encoding=utf-8
import sys
import time
import threading

import re

import chardet

"""
@author: v_jjyjiang 
@Description: 字符串常用工具类
@contact: jaey_summer@qq.com
@software: PyCharm
@file: stringtools.py
@time: 2018/4/17 20:36
"""


class StringUtils(object):
    def __init__(self):
        pass

    def __str__(self):
        super().__str__()

    def __del__(self):
        pass

    @staticmethod
    def to_utf8_string(str_bytes):
        """
        将GBK编码的bytes型数组转换成utf-8编码的str类型
        :param str_bytes: 传入一个bytes型字符串
        :return: 
        """
        string = None
        try:
            if StringUtils.string_is_no_empty(str_bytes):
                result = chardet.detect(str_bytes)
                # print("result%s" % result)
                if not (result["encoding"] == "utf-8"):
                    str_bytes = str_bytes.decode("gbk", "ignore")
                    str_bytes = str_bytes.encode("utf-8", "ignore")
                string = str_bytes.decode("utf-8")
            else:
                # string = " "
                pass
        except Exception as e:
            # print(e)
            string = str_bytes
        finally:
            return str(string)

    @staticmethod
    def string_is_no_empty(string):
        """
        传入一个字符串判断它是不是各种空
        :param string: 
        :return: 返回 true表示不是空  返回False表示是空的
        """
        result = True
        try:
            if string is None or string == "" or string == " " or string == u"" or string == u" ":
                result = False
        except Exception as e:
            print(e)
            pass

        return result

    @staticmethod
    def strings_is_no_empty(string, string_1):
        """
        传入两个字符串,先判断第一个是不是空,如果第一个是空,则不判断第二个了
        如果第一个不是空,则判断第二个
        :param string: 
        :return: 返回 true表示不是空  返回False表示是空的
        """
        result = [True, True]
        try:
            if string == "" or string == " " or string == u"" or string == u" " or string is None:
                result = [False, False]
            elif string_1 == "" or string_1 == " " or string_1 == u"" or string_1 == u" " or string_1 is None:
                result = [True, False]
        except Exception as e:
            print(e)
            pass

        return result

    @staticmethod
    def find_all_chinese(string):
        """
        传入一个字符串,返回字符串中包含的所有中文字符
        :param string: 字符串
        :return: list_str 一个列表,每一个值都是一个中文字符
        """
        string = StringUtils.to_utf8_string(string)
        list_str = re.findall(u'[\u4e00-\u9fa5]+', string)
        # print ("string: "+string)
        # print (list_str)
        # print result
        return list_str

    @staticmethod
    def find_all_character(string):
        """
        传入一个字符串,返回字符串中包含的所有字母字符
        :param string: 字符串
        :return: list_str 一个列表,每一个值都是一个字母字符
        """
        string = StringUtils.to_utf8_string(string)
        list_str = re.findall("[a-zA-Z0-9]+", string)
        # print ("string: "+string)
        # print (list_str)
        # print result
        return list_str

    @staticmethod
    def check_string_placeholder(string):
        """
        检查字符串中如果包含占位符标识%,那么他后面的标记符是否有被空格隔开
        缺陷: 如果是纯数字没有空格直接与%相连的场景,可能会误判为百分数,而不会做占位符处理
        :param string: 字符串
        :return: 返回True为正常,返回false为有误
        """

        result = True
        try:
            string = StringUtils.to_utf8_string(string)
            list_string = list(string)
            char_re = "%"
            pos = 0

            for string in list_string:
                if string == char_re:
                    if pos == 0:
                        if list_string[pos + 1] == " ":
                            result = False
                    elif pos >= 1:
                        if not re.findall("[0-9]", list_string[pos - 1]):
                            if not pos + 1 >= len(list_string):
                                if list_string[pos + 1] == " ":
                                    result = False
                        else:
                            # print 1
                            pass
                pos += 1

        except Exception as e:
            print(e)
            pass

        return result

    @staticmethod
    def compare_strings_placeholder(string_1, string_2):
        """
        用来检查基准字符串中如果包含一个占位符,那么用来做比对的字符串中占位符的格式也应该与基准字符串一致
        如: string_1中包含 %s,那么string_2中也需要有%s,而不是% s %d 等等错误表述
        该方法适合检查翻译后的文本占位符是否正确
        :param string_1: 传入一个作为基准的字符串
        :param string_2: 传入一个用来以基准字符串做比对的字符串
        :return: 返回True表示占位符的数量以及所有占位符后的标记都一样  返回False则存在不一样
        """
        result = True
        try:
            string_1 = StringUtils.to_utf8_string(string_1)
            string_2 = StringUtils.to_utf8_string(string_2)
            list_string_1 = list(string_1)
            list_string_2 = list(string_2)
            char_re = "%"
            list_re_ph = ["s", "d"]
            pos_1 = 0
            pos_2 = 0
            list_ph = []
            list_ph_2 = []

            for stri_1 in list_string_1:
                if stri_1 == char_re:
                    if not (pos_1 + 1) >= len(list_string_1):
                        if list_string_1[pos_1 + 1] in list_re_ph:
                            list_ph.append(list_string_1[pos_1 + 1])
                pos_1 += 1
            for stri_2 in list_string_2:
                if stri_2 == char_re:
                    if not (pos_2 + 1) >= len(list_string_2):
                        if list_string_2[pos_2 + 1] in list_re_ph:
                            list_ph_2.append(list_string_2[pos_2 + 1])
                pos_2 += 1
            if len(list_ph) != len(list_ph_2):
                result = False
            else:
                for ph in list_re_ph:
                    if not list_ph.count(ph) == list_ph_2.count(ph):
                        result = False

        except Exception as e:
            print(e)
            pass
        return result

    @staticmethod
    def compare_strings_escape(string_1, string_2):
        """
        用来检查基准字符串中如果包含一个转义字符,那么用来做比对的字符串中转义字符的格式也应该与基准字符串一致
        如: string_1中包含 \n,那么string_2中也需要有\n,而不是\ n, \t 等等错误表述
        该方法适合检查翻译后的文本转义字符是否正确
        :param string_1: 传入一个作为基准的字符串
        :param string_2: 传入一个用来以基准字符串做比对的字符串
        :return: 返回True表示转义字符的数量以及所有转义字符后的标记都一样  返回False则存在不一样
        """
        result = True
        try:
            string_1 = StringUtils.to_utf8_string(string_1)
            string_2 = StringUtils.to_utf8_string(string_2)

            list_char = [r"\n", r"\t", r"\\n", r"\\t"]

            list_string = []
            list_string_2 = []

            for char in list_char:
                list_temp = re.findall(char, string_1)

                list_temp_2 = re.findall(char, string_2)

                if len(list_temp) > 0:
                    list_string = list_string + list_temp
                if len(list_temp_2) > 0:
                    list_string_2 = list_string_2 + list_temp_2

            # print(list_string)
            # print(list_string_2)
            if len(list_string) > 0:
                if len(list_string) != len(list_string_2):
                    result = False
                else:
                    for string in list_string:
                        if not (string in list_string_2):
                            result = False
        except Exception as e:
            print(e)
            pass
        return result

    @staticmethod
    def check_strings_twin_mark(string):
        """
        用来检查一个字符串中,本应成对存在的符号,是否没有成对出现,存在遗漏
        :param string: 传入一个字符串
        :return: 返回True表示所有应该成对出现的符号都成对出现了  返回False则存在问题
        """
        string = StringUtils.to_utf8_string(string)
        result = True
        try:
            list_string_1 = list(string)
            list_char = ["\""]
            list_char_2 = [("{", "}"), ("[/", "/]")]
            pos_1 = 0
            list_pos_1 = []
            for stri_1 in list_string_1:
                # 循环list_char的检查项,并添加进复数检查的集合中
                if stri_1 in list_char:
                    if not (pos_1 + 1) > len(list_string_1):
                        list_pos_1.append(list_string_1[pos_1])

                # 循环list_char_2的检查项,并给出结果
                for array in list_char_2:
                    if string.find(array[0]) != -1:
                        if string.find(array[1]) == -1:
                            result = False
                    if string.find(array[1]) != -1:
                        if string.find(array[0]) == -1:
                            result = False
                pos_1 += 1
            # 计算这个集合里存储的数据总量是单数还是双数,如果是单数,则返回false
            if not len(list_pos_1) % 2 == 0:
                result = False
        except Exception as e:
            print(e)
            pass
        return result

    @staticmethod
    def check_strings_multi_blank(string):
        """
        用于检查一个字符串中,句子中间不存在2个以上的空格, 不包含句首和句末
        :param string: 传入一个字符串
        :return: 返回True表示句中不存在两个以上空格  返回False则存在问题
        """
        result = True
        try:

            string = StringUtils.to_utf8_string(string)
            list_string = list(string.strip())
            i = 0
            for stri in list_string:
                if stri == " ":
                    if i > 0 and list_string[i - 1] == " ":
                        result = False
                        break
                i += 1
        except Exception as e:
            print(e)
            pass
        return result

    @staticmethod
    def compare_strings_twin_mark(string_1, string_2):
        """
        用来对比一组字符串中,第一个字符串中存在的标签在第二个字符串中是否也对应存在
        :param string_2: 
        :param string_1 
        传入一组字符串
        :return: 返回True
        """
        string_1 = StringUtils.to_utf8_string(string_1)
        string_2 = StringUtils.to_utf8_string(string_2)
        # list_string_1 = []
        # list_string_2 = []
        result = True
        try:
            list_chars = [("[/", "/]")]
            for index in range(len(list_chars)):
                if string_1.find(list_chars[index][0]) != -1 and string_1.find(list_chars[index][1]) != -1:
                    if (string_2.find(list_chars[index][0]) == -1 or string_2.find(list_chars[index][1])) == -1:
                        result = False
        except Exception as e:
            print(e)
            pass
        return result

    @staticmethod
    def compare_strings_sign_inner(string_1, string_2):
        """
        用来检查基准字符串中如果包含如:两个括号之间的内容{0:d},那么对比的字符串中,这部分内容出现的次数,以及其中的值,也应该一致
        如: string_1中包含{0:d}{1:d},那么string_2中也需要有{0:d}{1:d}
        :param string_1: 传入一个作为基准的字符串
        :param string_2: 传入一个用来以基准字符串做比对的字符串
        :return: 返回True表示标记内容出现的次数和里面的内容都没有问题   返回False表示有错误
        """
        result = True
        try:
            string_1 = StringUtils.to_utf8_string(string_1)
            string_2 = StringUtils.to_utf8_string(string_2)
            list_string_1 = []
            list_string_2 = []
            # char_re = ".*?\\[(.*?)\\].*?"
            # print(re.findall(char_re,string_1))
            char_re = ".*?\\{0:s}(.*?)\\{1:s}.*?"
            list_re_ph = [("{", "}"), ("[", "]")]
            list_re = []
            for re_temp in list_re_ph:
                list_re.append(char_re.format(re_temp[0], re_temp[1]))
            # print(list_re)
            for re_run in list_re:
                # print(re.findall(re_run, string_1))
                list_string_1.extend(re.findall(re_run, string_1))
                list_string_2.extend(re.findall(re_run, string_2))
                # print(list_string_1)
            for string in list_string_1:
                if string not in list_string_2:
                    result = False
        except Exception as e:
            print(e)
            pass
        return result

    @staticmethod
    def compare_strings_label_content(string_1, string_2):
        """
        用来检查基准字符串中如果包含如:两个尖括号<>之间的内容<Setting_Font03>,那么对比的字符串中,这部分内容出现的次数,以及其中的值,也应该一致
        如: string_1中包含<Setting_Font03>,那么string_2中也需要有<Setting_Font03>
        :param string_1: 传入一个作为基准的字符串
        :param string_2: 传入一个用来以基准字符串做比对的字符串
        :return: 返回True表示标记内容出现的次数和里面的内容都没有问题   返回False表示有错误
        """
        result = True
        try:
            string_1 = StringUtils.to_utf8_string(string_1)
            string_2 = StringUtils.to_utf8_string(string_2)
            list_string_1 = []
            list_string_2 = []
            char_re = ".*?\\{0:s}(.*?)\\{1:s}.*?"
            list_re_ph = [("<", ">")]
            list_re = []
            for re_temp in list_re_ph:
                list_re.append(char_re.format(re_temp[0], re_temp[1]))
            # print(list_re)
            for re_run in list_re:
                # print(re.findall(re_run, string_1))
                list_string_1.extend(re.findall(re_run, string_1))
                # print(list_string_1)
                list_string_2.extend(re.findall(re_run, string_2))
                # print(list_string_1)
            if not len(list_string_1) == len(list_string_2):  # 先判断两个集合中标签的数量是否一致
                result = False
            else:
                for index in range(len(list_string_1)):  # 判断各个下标对应的标签的key是否一致
                    if not list_string_1[index] == list_string_2[index]:
                        result = False
        except Exception as e:
            print(e)
            pass
        return result

    @staticmethod
    def compare_strings_label_attributes(string_1, string_2):
        """
        用来检查基准字符串中如果包含如:单标签之间的属性和元素<img src=$$GoldImage$$/>,那么对比的字符串中,这部分内容出现的次数,以及其中的值,也应该一致
        如: string_1中包含<img src=$$GoldImage$$/>,那么string_2中也需要有<img src=$$GoldImage$$/>
        :param string_1: 传入一个作为基准的字符串
        :param string_2: 传入一个用来以基准字符串做比对的字符串
        :return: 返回True表示标记内容出现的次数和里面的内容都没有问题   返回False表示有错误
        """
        result = True
        try:
            string_1 = StringUtils.to_utf8_string(string_1)
            string_2 = StringUtils.to_utf8_string(string_2)
            list_string_1 = []
            list_string_2 = []
            char_re = ".*?\\{0:s}(.*?)\\{1:s}.*?"
            list_re_ph = [("<", ">"), ("<", "/>")]
            list_re = []
            for re_temp in list_re_ph:
                list_re.append(char_re.format(re_temp[0], re_temp[1]))
            # print(list_re)
            # print(re.findall(list_re[0], string_1))
            for re_run in list_re:
                # print(re.findall(re_run, string_1))
                list_string_1.extend(re.findall(re_run, string_1))
                # print(list_string_1)
                list_string_2.extend(re.findall(re_run, string_2))
                # print(list_string_2)
            for string in list_string_1:
                if string not in list_string_2:
                    result = False
        except Exception as e:
            print(e)
            pass
        return result

    @staticmethod
    def compare_strings_brackets_content(string_1, string_2):
        """
        用来检查基准字符串中如果包含如:两个括号之间的内容[ffff33],那么对比的字符串中,这部分内容出现的次数,以及其中的值,也应该一致
        如: string_1中包含[ffff33],那么string_2中也需要有[ffff33]
        :param string_1: 传入一个作为基准的字符串
        :param string_2: 传入一个用来以基准字符串做比对的字符串
        :return: 返回True表示标记内容出现的次数和里面的内容都没有问题   返回False表示有错误
        """
        result = True
        try:
            string_1 = StringUtils.to_utf8_string(string_1)
            string_2 = StringUtils.to_utf8_string(string_2)
            list_string_1 = []
            list_string_2 = []
            char_re = ".*?\\{0:s}(.*?)\\{1:s}.*?"
            list_re_ph = [("[", "]")]
            re_color = "^[a-fA-F0-9]{6}$"
            list_re = []
            for re_temp in list_re_ph:
                list_re.append(char_re.format(re_temp[0], re_temp[1]))

            for re_run in list_re:
                for temp in re.findall(re_run, string_1):
                    temp = temp.upper()
                    # print("1: %s"%temp)
                    temp = re.findall(re_color, temp)
                    # print("2",end="")
                    # print(temp)
                    if len(temp) > 0:
                        list_string_1.extend(temp)
                for temp in re.findall(re_run, string_2):
                    temp = temp.upper()
                    temp = re.findall(re_color, temp)
                    if len(temp) > 0:
                        list_string_2.extend(temp)

            for string in list_string_1:
                if string not in list_string_2:
                    result = False
        except Exception as e:
            print(e)
            pass
        return result

    @staticmethod
    def compare_strings_num(string_1, string_2):
        """
        用来检查基准字符串中如果包含一个数字字符串,那么用来做比对的字符串中数字字符串的格式也应该与基准字符串一致
        如: string_1中包含 1000,那么string_2中也需要有1000,而不是100, 10000 等等错误表述
        该方法适合检查翻译后的文本数字字符串是否正确
        :param string_1: 传入一个作为基准的字符串
        :param string_2: 传入一个用来以基准字符串做比对的字符串
        :return: 返回True表示数字字符串没有变化  返回False则存在不一样
        """
        result = True
        try:
            string_1 = StringUtils.to_utf8_string(string_1)
            string_2 = StringUtils.to_utf8_string(string_2)
            char_re = "\d+\.?\d*"
            list_base_string_1 = re.findall(char_re, string_1)
            list_base_string_2 = re.findall(char_re, string_2)
            list_string_1 = []
            list_string_2 = []
            # print(list_base_string_1)
            # print(list_base_string_2)
            for string in list_base_string_1:
                length = len(string)
                pos = string.rfind(".")
                if length - 1 == pos:
                    string = string[0:pos]
                list_string_1.append(string)
                # print(string)
            # print(list_string_1)
            for string in list_base_string_2:
                length = len(string)
                pos = string.rfind(".")
                if length - 1 == pos:
                    string = string[0:pos]
                list_string_2.append(string)
            # print(list_string_2)
            for stri in list_string_1:
                if not (stri in list_string_2):
                    result = False
        except Exception as e:
            print(e)
        return result

    d = 0

    @staticmethod
    def check_string_exist_blacklist(string):
        """
        检查字符串中是否存在黑名单列表里出现的内容
        :param string: 传入一个字符串
        :return: 返回True表示句中不存在两个以上空格  返回False则存在问题
        """
        result = True, None
        try:
            # print("行数: %d :  字符串: %s" % (StringUtils.d, string))
            # print(StringUtils.d)
            StringUtils.d += 1
            string = StringUtils.to_utf8_string(string)
            list_blacklist = {
                0x00: '#NULL!',  # Intersection of two cell ranges is empty
                0x07: '#DIV/0!',  # Division by zero
                0x0F: '#VALUE!',  # Wrong type of operand
                0x17: '#REF!',  # Illegal or deleted cell reference
                0x1D: '#NAME?',  # Wrong function or range name
                0x24: '#NUM!',  # Value range overflow
                0x2A: '#N/A',  # Argument or function not available
            }
            if string in list_blacklist.keys():
                result = False, string
        except Exception as e:
            print(e)
            pass
        return result

    @staticmethod
    def check_en_string_exist_cn(string):
        """
        检查英文字符串中是否包含中文
        :param string: 传入一个字符串
        :return: 返回True表示正常(英文中不包含中文)  返回False表示报警(英文中包含了中文)
        """
        result = True
        try:
            string = StringUtils.to_utf8_string(string)
            if StringUtils.find_all_chinese(string):
                result = False
            pass

        except Exception as e:
            print(e)
            pass
        return result

    @staticmethod
    def compare_strings_length(string_1, string_2, threshold):
        """
        用来检查基准字符串
        :param string_1: 传入一个作为基准的字符串
        :param string_2: 传入一个用来以基准字符串做比对的字符串
        :param threshold 阈值(函数内部将其转成百分比)
        :return: 返回True表示没有超过阈值, False表示超过了阈值
        """
        result = True
        try:
            string_1 = StringUtils.to_utf8_string(string_1)
            string_2 = StringUtils.to_utf8_string(string_2)
            # 将阈值转成百分小数
            threshold = threshold / 100
            # print("len_1:", end=" ")
            # print(len(string_1))
            # print("len_2:", end=" ")
            # print(len(string_2))
            # print("len_2/len_1:", end=" ")
            # print("threshold:", end=" ")
            # print(threshold)
            # print(len(string_2) / len(string_1))
            if len(string_2) / len(string_1) > threshold:
                result = False
        except Exception as e:
            print(e)
        return result

    @staticmethod
    def check_string_head_ending(string_1):
        """
        用来检查基准字符串
        :param string_1: 传入一个作为字符串
        :return: 返回True表示头尾都没有空格或换行, False表示头尾有空格或换行
        """
        result = True
        try:
            string_1 = StringUtils.to_utf8_string(string_1)
            length = len(string_1)
            hb_pos = string_1.find(" ")
            # print(hb_pos)
            eb_pos = string_1.rfind(" ")
            # print(eb_pos)
            hl_pos = string_1.find("\n")
            # print(hl_pos)
            el_pos = string_1.rfind("\n")
            # print(el_pos)
            ht_pos = string_1.find("\t")
            et_pos = string_1.find("\t")
            if hb_pos == 0 or hl_pos == 0 or eb_pos == (length - 1) or el_pos == (length - 1) or ht_pos == 0 or et_pos == (length - 1):
                result = False
        except Exception as e:
            print(e)
        return result


if __name__ == '__main__':
    pass
