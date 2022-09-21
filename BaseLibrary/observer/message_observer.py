import abc
import threading
from queue import Queue

"""
@author: v_jjyjiang 
@Description: 实现一个观察者模式的消息传递的方式
@contact: jaey_summer@qq.com
@software: PyCharm
@file: message_observer.py
@time: 2018/5/11 20:03
"""


class PropertyObservable(object):
    def __init__(self):
        # 添加监听者集合
        self.__list_listener = {}

        # 消息队列
        self.__queue = Queue()

    def __str__(self):
        return super().__str__()

    def __del__(self):
        pass

    def get_listener_count(self, msg_id):
        """
        或取对msgID这个消息监听的数目
        :param msg_id: 
        :return: listps的长度xx
        """
        list_ps = self.__list_listener.get(msg_id)
        if list_ps is not None:
            return len(list_ps)
        return 0

    def add_listener(self, listener, list_msg_id=None):
        """
        添加监听者和需要监听的消息
        :param list_msg_id: 
        :param listener: 
        :param msg_id: 
        :return: 
        """
        if list_msg_id is None:
            list_msg_id = []
        if listener is not None:
            for i in list_msg_id:
                self.__list_listener[i] = listener


    def remove_listener(self, listener, list_msg_id):
        if list_msg_id is None:
            list_msg_id = []
        if listener is not None:
            for i in list_msg_id:
                self.__list_listener.pop(i)

    def fire_event(self, sender, msg_id, args=None):
        if args is None:
            args = []
        listener = self.__list_listener.get(msg_id)
        if listener is None:
            return
        try:
            # TODO 队列回调(暂时不用这个)
            # post = threading.Thread(target=self.receive, args=(self.queue, [sender, msg_id, args]))
            # post.setDaemon(True)
            # post.start()
            # send = threading.Thread(target=self.send, args=(self.queue, listener))
            # send.setDaemon(True)
            # send.start()

            # 自然回调
            listener.on_message_receive(sender, msg_id, args)
        except Exception as e:
            print(e)

    def __receive(self, queue, args=None):
        if args is None:
            args = []
        queue.put(args)

    def __send(self, queue, listener):
        while True:
            args = queue.get()
            print(args)
            listener.on_message_receive(args[0], args[1], args[2])
            if queue.empty():
                break


# 队列回调可选用 TODO 实现中
class PostThread(threading.Thread):
    """
    使用线程队列传递消息
    """

    def __init__(self, queue, sender, msg_id, list_arg=None, group=None, target=None,
                 name=None, args=(), kwargs=None, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.q = queue
        # self.listener = listener
        self.sender = sender
        self.msg_id = msg_id
        self.args = list_arg

    def run(self):
        """
       消息传递线程函数
       :param listener: 
       :param sender: 
       :param msg_id: 
       :param args: 
       :return: 
       """
        if self.args is None:
            args = []
        self.q.put((self.sender, self.msg_id, self.args))
        # self.q.put(self.listener.on_message_receive(self.sender, self.msg_id, self.args))


class PropertyListener(object):
    """
     观察者的回调接口方法. sender是否为null取决于被观察者激发一个消息时的设置, 通常可以根据sender==this来判断是否是自己激发的事件
     此方法中不能更新UI线程,必须放到主线程进行更新
    """

    @abc.abstractmethod
    def on_message_receive(self, sender, msg_id, args):
        raise NotImplementedError("你必须先实现这个抽象方法!")


if __name__ == '__main__':
    pass
