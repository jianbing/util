#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import functools
import threading
import ctypes
"""
启动一个后台线程，随时可以结束掉它。
"""


class TaskService:
    _tasks = dict()

    @classmethod
    def register(cls, task_name, ident):
        cls._tasks[task_name] = ident

    @classmethod
    def have(cls, task_name):
        if task_name in cls._tasks:
            print("task {} is already exists".format(task_name))
            return True
        return False

    @classmethod
    def stop(cls, task_name):
        if task_name not in cls._tasks:
            print("task {} is not exists".format(task_name))
            return
        tid = cls._tasks[task_name]
        exc_type = SystemExit
        tid = ctypes.c_long(tid)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
        del cls._tasks[task_name]

        if res == 0:
            raise ValueError("invalid thread id，the task may be already stop")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


def background_task(task_name):
    def warp(func):
        @functools.wraps(func)
        def _wrap(*args, **kwargs):
            if TaskService.have(task_name):
                return
            try:
                t = threading.Thread(target=func, args=args, kwargs=kwargs)
                t.start()
                TaskService.register(task_name, t.ident)
            except Exception:
                import traceback
                traceback.print_exc()

        return _wrap

    return warp


