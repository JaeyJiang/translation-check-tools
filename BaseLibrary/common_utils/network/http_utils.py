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


class HTTPUtils(object):
    def __init__(self):
        pass

    def __str__(self):
        return super().__str__()

    def __del__(self):
        pass

    class Builder(object):
        def __init__(self):
            self.__headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8",
                "Cache-Control": "max-age=0", "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13059.400"}
            self.__type_req = "GET"
            self.__url = None
            self.__params = "{'test','none'}"
            self.__proxy = None
            self.__request = None
            self.response_code = None

        def set_url(self, url):
            """
            设置请求地址
            :param url
            :return: Builder
            """
            self.__url = url
            return self

        def set_params(self, params):
            """
            设置请求参数, get/post参数均使用此格式 如:{"a":xxxx,"b":"bbbb"} 字典类型
            :param params: 请求参数
            :return: self
            """

            self.__params = params
            return self

        def set_proxy(self, proxy):
            """
            设置代理方式和地址 格式如: {'http': "http://web-proxy.tencent.com:8080/"},{'https': "https://web-proxy.tencent.com:8080/"}
            :param proxy: 
            :return: self
            """
            self.__proxy = proxy
            # self.__request = self.__set_proxy_request()
            return self

        def __set_proxy_request(self):
            try:
                proxy_set = urllib.request.ProxyHandler(self.__proxy)
                request = urllib.request.Request(url=self.__url, method=self.__type_req, headers=self.__headers)
                http_handler = urllib.request.HTTPHandler(debuglevel=1)
                https_handler = urllib.request.HTTPSHandler(debuglevel=1)
                opener = urllib.request.build_opener(proxy_set, http_handler, https_handler)
                urllib.request.install_opener(opener)
                return request
            except ValueError as e:
                print("请先使用set_url函数,设置url")
                raise ValueError

        def set_headers(self, headers):
            """
            设置headers
            :param headers: 
            :return: self
            """
            self.__headers = headers
            return self

        def get(self):
            """
            返回get请求的结果 byte型
            :return: 
            """
            result_bytes = None
            try:
                self.__params = urllib.parse.urlencode(self.__params)
                self.__url += self.__params
                self.__type_req = "GET"
                if self.__proxy is None:
                    self.__request = urllib.request.Request(url=self.__url, method=self.__type_req, headers=self.__headers)
                else:
                    self.__request = self.__set_proxy_request()
                response = urllib.request.urlopen(self.__request)
                self.response_code = response.getcode()
                result_bytes = response.read()
            except Exception as e:
                print("Get_error", end="\t")
                print(e)
                result_bytes = e
                self.response_code = 504
            finally:
                return result_bytes

        def post(self):
            """
            返回post请求的结果 byte型
            :return: 
            """
            result_bytes = None
            try:
                self.__type_req = "POST"
                if self.__proxy is None:
                    self.__request = urllib.request.Request(url=self.__url, method=self.__type_req, headers=self.__headers)
                else:
                    self.__request = self.__set_proxy_request()
                self.__params = json.dumps(self.__params).encode('utf8')
                print(self.__params)
                response = urllib.request.urlopen(url=self.__request, data=self.__params)
                self.response_code = response.getcode()
                result_bytes = response.read()
            except Exception as e:
                print("Post_error", end="\t")
                print(e)
                result_bytes = e
                self.response_code = 504
            finally:
                return result_bytes


if __name__ == '__main__':
    pass
