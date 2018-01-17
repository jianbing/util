#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created by jianbing on 2018-01-17
"""
from util.tool.btask import background_task, TaskService

if __name__ == '__main__':

    import time


    @background_task("a_background_job")
    def hi(name):
        while 1:
            print("hi, {}".format(name))
            time.sleep(1)


    hi("jianbing")

    time.sleep(5)
    TaskService.stop("a_background_job")
    print("stop")