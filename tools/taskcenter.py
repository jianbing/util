#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import queue
import threading
import time
import types


class TaskCenter(object):
    """
    任务执行器，多线程方式
    """

    def __init__(self, target, param_list, thread_num, allow_append_param=False):
        """初始化

        :param target: 任务函数
        :param param_list: 包含需要处理的全部参数的列表，多个参数的，使用tuple方式，如 [(1,2,3),(3,)]，单个参数的，直接加入list
        :param thread_num: 任务线程数量
        :param allow_append_param:是否支持执行期间继续添加参数，如果True，则任务线程get不到参数时，会阻塞等待
        :return:
        """
        self.__target = target
        self.__param_list = param_list
        self.__thread_num = thread_num
        self.__param_queue = queue.Queue()
        self.__allow_append_param = allow_append_param
        self.__thread_dict = dict()

    def __init_param_queue(self):
        """初始化参数列表

        :return:
        """
        for i in self.__param_list:
            self.__param_queue.put(i)
        if not self.__allow_append_param:
            self.__add_finish_param()

    def __add_finish_param(self):
        """设置完成任务的标记，任务线程接收到None时，会结束线程

        :return:
        """
        for i in range(self.__thread_num):
            self.__param_queue.put(None)

    def __thread_func(self):
        while True:
            args = self.__param_queue.get()
            if args:
                if isinstance(args, tuple):
                    self.__target(*args)
                else:
                    self.__target(args)
                self.__param_queue.task_done()
            else:
                break

    def start(self):
        self.__init_param_queue()
        for i in range(1, self.__thread_num+1):
            self.__thread_dict[i] = threading.Thread(target=self.__thread_func)
            self.__thread_dict[i].start()

    def wait_to_finish(self):
        """调用后，会阻塞主线程，直到全部任务线程结束，不允许继续新增任务函数参数

        :return:
        """
        self.finish_append_params()
        for i in self.__thread_dict:
            self.__thread_dict[i].join()

    def append_params(self, param_list):
        if self.__allow_append_param:
            for i in param_list:
                self.__param_queue.put(i)
        else:
            raise Exception("不可以添加新的参数列表")

    def finish_append_params(self):
        self.__allow_append_param = False
        self.__add_finish_param()


if __name__ == '__main__':

    from utils.decorators import retry

    def to_download(astr):
        print("{0}___________".format(astr))
        time.sleep(1)

    start_time = time.time()

    params = []
    for i in range(2):
        for ii in range(6):
            params.append("{0}_{1}".format(i,ii))

    params.append(("hello world",))

    center = TaskCenter(target=retry()(to_download), param_list=params, thread_num=1)
    center.start()
    center.wait_to_finish()

    print('finish')
    print(time.time()-start_time)



