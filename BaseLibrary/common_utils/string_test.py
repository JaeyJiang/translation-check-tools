# encoding=utf-8

"""
@author: v_jjyjiang 
@Description: TODO(这里用一句话描述这个模块的作用)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: string_test.py
@time: 2018/4/16 20:44
"""
import datetime
import os

import sys

import re

import time

from BaseLibrary.common_utils.stringutils import StringUtils


class StringTest(object):
    __instance = None

    def __init__(self):
        self.string_1 = "asd1000as\td%sa50sd%\nd10%smmma500%d sdlk"
        self.string_2 = "卧槽%s哈\t哈%d\n嘻1000嘻10%c50c%s哈哈500%哈"
        self.string_3 = "asdasd\',哈哈\' 你妹的 嘻嘻 [sd啊 {asd},\"asd\""
        self.string_4 = "您确定要开始新游戏吗?\\n之后您还可以通过FB或GP账号登录，载入当前游戏数据。"
        self.string_5 = "您確定要開始新遊戲嗎？\\n之後您還可以通過Facebook或Google Play帳號登入，載入當前遊戲數據。"

    def __str__(self):
        return super().__str__()

    def __del__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance


if __name__ == '__main__':
    st = StringTest()
    # print(st)
    # list_str = StringUtils.find_all_chinese(st.string_1)
    # print list_str
    # for string in list_str:
    #     string = string.encode("utf-8")
    #     print string
    # print("哈哈")

    # print StringUtils.check_string_placeholder(st.string_2)
    # print(StringUtils.compare_strings_placeholder(st.string_1, st.string_2))
    # print StringUtils.compare_strings_escape(st.string_1,st.string_2)
    # print StringUtils.check_strings_twin_mark(st.string_3)

    # print StringUtils.check_strings_multi_blank(st.string_3)

    # print StringUtils.compare_strings_num(st.string_1,st.string_2)

    # print StringUtils.string_is_no_empty(st.string_4)

    # dict_1 = {}
    #
    # i = 0
    # while i < 10:
    #     dict_1[i] = []
    #     j = 0
    #     while j < 10:
    #         dict_1[i].append([(i, j), "aa %d" % j])
    #         j += 1
    #     i += 1
    #
    # for item_data in dict_1.items():
    #     print(item_data)

    # temp = ["1","2","3","4"]
    # temp = '+'.join(temp)
    # print(temp)
    # string = "[FFBBFF] asd, {aaaaa} (1123123)"
    # string2 = "[FFBBFF] asd, {aaaaa}"
    # print(StringUtils.compare_strings_sgin_inner( string,string2))
    # print(StringUtils.compare_strings_escape(st.string_4, st.string_5))

    # char = r"\\n"
    # print(re.findall(char, st.string_4))

    # a = [[1, 2, 3]]
    # c = a
    # b = a.copy()
    # a[0] = [1, 2]
    # print(a)
    # print(b)
    # print(c)

    # try:
    #     pass
    #
    # except ValueError as e:
    #     print("Exception: %s" % e)
    #     print("请不要输入字母")

    # string_1 = " 哈哈[FFaA10] [嘻嘻]嘻嘻"
    # string_2 = " 呵呵[ffaa10] [哈哈]嘻嘻"
    # print(StringUtils.compare_strings_brackets_content(string_1, string_2))
    string_1 = ";位/于?战:场@最&中=心+，$象,征至高无上的权利，是主要的争夺建筑之一。持续占领时，每分钟增加200点势力积分，和20点个人积分。"
    string_2 = "This building is located at the center of the map and symbolizes power, and it's哈哈 one of the main buildings players fight to capture. Once it's been captured, the occupier earns 200 faction points and 20 personal points every minute.位於戰場最中心，象徵至高無上的權利，是主要的爭奪建築之一。佔領後，每分鐘增加150點勢力積分，和15點個人積分。"
    # print(StringUtils.check_string_exist_blacklist(string_1))

    # print(StringUtils.compare_strings_label_attributes(string_1,string_2))

    # print(StringUtils.compare_strings_label_content(string_1, string_2))
    #
    # print(StringUtils.compare_strings_num("11", "1"))
    #
    # string_3 = "Threshold=100"
    # pos = string_3.rfind("=")
    # print(pos)
    # print(string_3[0:pos])
    # print(string_3[pos + 1:])
    #
    # print(StringUtils.compare_strings_length(string_1, string_2, 200))
    #

    # list_str = re.findall("[;\/\?:@&=\+$,#]",string_1)
    # print(list_str)

    # string = "a as"
    # print("length: %s"%len(string))
    # print(StringUtils.check_string_head_ending(string))

    temp_time_1 = datetime.datetime.now()

    print(temp_time_1)
    a = 1
    for i in range(100000):
        a = a*(i+1)

    temp_time_2 = datetime.datetime.now()

    print(temp_time_2)

    print((temp_time_2-temp_time_1).seconds)
