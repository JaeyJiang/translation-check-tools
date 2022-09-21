import json
import sys
import time
import threading
import urllib.error
import urllib.parse
import urllib.request

"""
@author: v_jjyjiang 
@Description: TODO(这里用一句话描述这个模块的作用)
@contact: jaey_summer@qq.com
@software: PyCharm
@file: http_utils.py
@time: 2018/9/18 15:35
"""


class HTTPBaseUtils(object):
    def __init__(self, url, type_req, params=None, headers=None, proxy=None):
        if headers is not None:
            self.__headers = headers
        else:
            self.__headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8",
                "Cache-Control": "max-age=0", "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13059.400"}
        self.__url = url
        self.__type_req = type_req
        if params is not None:
            self.__params = urllib.parse.urlencode(params)  # urllib生成get/post参数  类似 a=x&b=y 这样的
            if self.__type_req is "GET" or self.__type_req is "get":
                self.__url += self.__params
        self.__proxy = None
        if proxy is not None:
            self.__proxy = proxy

    def __str__(self):
        return super().__str__()

    def __del__(self):
        pass

    def get_request(self):
        req = urllib.request.Request(url=self.__url, method=self.__type_req, headers=self.__headers)
        if self.__proxy is not None:
            req = self.__set_proxy_request()
        response = urllib.request.urlopen(req)
        result_bytes = response.read()
        return result_bytes

    def post_request(self):
        req = urllib.request.Request(url=self.__url, method=self.__type_req, headers=self.__headers)
        if self.__proxy is not None:
            req = self.__set_proxy_request()
        response = urllib.request.urlopen(req, self.__params)
        result_bytes = response.read()
        return result_bytes

    def __set_proxy_request(self):
        proxy_set = urllib.request.ProxyHandler(self.__proxy)
        request = urllib.request.Request(url=self.__url, method=self.__type_req, headers=self.__headers)
        http_handler = urllib.request.HTTPHandler(debuglevel=1)
        https_handler = urllib.request.HTTPSHandler(debuglevel=1)
        opener = urllib.request.build_opener(proxy_set, http_handler, https_handler)
        urllib.request.install_opener(opener)
        return request


if __name__ == '__main__':
    pass
