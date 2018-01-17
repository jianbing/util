#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import threading
import time
import os
import sys
import platform
import functools


def chdir(dir_path=''):
    """自动调用os.chdir

    :param dir_path:
    :return:
    """
    def _chdir(func):
        @functools.wraps(func)
        def __chdir(*args, **kwargs):
            os.chdir(dir_path)
            return func(*args, **kwargs)
        return __chdir
    return _chdir


def retry(times=5):
    """一个装饰器，可以设置报错重试次数

    :param times: 最多重试次数
    :return:
    """
    def _retry(func):
        @functools.wraps(func)
        def __retry(*args, **kwargs):
            retry_times = 0
            while retry_times <= times:
                try:
                    res = func(*args, **kwargs)
                    return res
                except Exception:
                    print(sys.exc_info()[1])
                    retry_times += 1
                    if retry_times <= times:
                        print('1秒后重试第{0}次'.format(retry_times))
                        time.sleep(1)
            else:
                print('max try,can not fix')
                import traceback
                traceback.print_exc()
                return None
        return __retry
    return _retry


def count_running_time(func):
    """装饰器函数，统计函数的运行耗时

    :param func:
    :return:
    """
    @functools.wraps(func)
    def _count_running_time(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(('cost time :{:.3f}'.format(time.time() - start)))
        return res
    return _count_running_time


def auto_next(func):
    """可以给协程用，自动next一次

    :param func:
    :return:
    """
    @functools.wraps(func)
    def _auto_next(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g
    return _auto_next


def check_adb(func):
    @functools.wraps(func)
    def _check_adb(*args, **kwargs):

        @cache_result()
        def get_adb_devices():
            from util.common import run_cmd
            return run_cmd('adb devices')

        result = get_adb_devices()
        if(len(result)) < 2:
            print('当前没有连接上手机')
            return None
        return func(*args, **kwargs)
    return _check_adb


def cache_result(times=60):
    def _wrap(func):
        @functools.wraps(func)
        def __wrap(*args, **kwargs):

            if hasattr(func, "__last_call_result__") and time.time() - func.__last_call_time__ < times:
                print(func.__last_call_result__)
                return func.__last_call_result__
            else:
                result = func(*args, **kwargs)
                func.__last_call_result__ = result
                func.__last_call_time__ = time.time()
                return result
        return __wrap
    return _wrap


def windows(func):
    """如果非windows系统，抛出异常

    :param func:
    :return:
    """

    if not platform.platform().startswith('Windows'):
        raise Exception("This function just can be used in windows.")
    return func


class Singleton(object):
    """单例模式，python最佳的单例方式还是通过模块来实现

    用法如下:
        @Singleton
        class YourClass(object):
    """

    def __init__(self, cls):
        self.__instance = None
        self.__cls = cls
        self._lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        self._lock.acquire()
        if self.__instance is None:
            self.__instance = self.__cls(*args, **kwargs)
        self._lock.release()
        return self.__instance


def simple_background_task(func):
    @functools.wraps(func)
    def _wrap(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
        return
    return _wrap
