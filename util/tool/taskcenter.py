#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import queue
import threading
import time


class TaskCenter:
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
        self._target = target
        self._param_list = param_list
        self._thread_num = thread_num
        self._param_queue = queue.Queue()
        self._allow_append_param = allow_append_param
        self._thread_dict = dict()

    def _init_param_queue(self):
        """初始化参数列表

        :return:
        """
        for i in self._param_list:
            self._param_queue.put(i)
        if not self._allow_append_param:
            self._add_finish_param()

    def _add_finish_param(self):
        """设置完成任务的标记，任务线程接收到None时，会结束线程

        :return:
        """
        for i in range(self._thread_num):
            self._param_queue.put("__finish__")

    def _thread_func(self):
        while True:
            args = self._param_queue.get()
            print("参数列表剩余：{}组".format(self._param_queue.qsize()))
            if args is not "__finish__":
                if isinstance(args, tuple):
                    self._target(*args)
                else:
                    self._target(args)
                self._param_queue.task_done()
            else:
                break

    def start(self):
        self._init_param_queue()
        for i in range(1, self._thread_num+1):
            self._thread_dict[i] = threading.Thread(target=self._thread_func)
            self._thread_dict[i].start()

    def wait_to_finish(self):
        """调用后，会阻塞主线程，直到全部任务线程结束，不允许继续新增任务函数参数

        :return:
        """
        self.finish_append_params()
        for i in self._thread_dict:
            self._thread_dict[i].join()

    def append_params(self, param_list):
        if self._allow_append_param:
            for i in param_list:
                self._param_queue.put(i)
        else:
            raise Exception("不可以添加新的参数列表")

    def finish_append_params(self):
        self._allow_append_param = False
        self._add_finish_param()


if __name__ == '__main__':

    from util.decorator import retry

    def to_download(astr):
        print("{0}___________".format(astr))
        time.sleep(1)

    start_time = time.time()

    params = []
    for i in range(2):
        for ii in range(6):
            params.append("{0}_{1}".format(i,ii))

    params.append(("hello world",))
    print(len(params))
    print(params)
    center = TaskCenter(target=retry()(to_download), param_list=params, thread_num=2)
    center.start()
    center.wait_to_finish()

    print('finish')
    print(time.time()-start_time)



