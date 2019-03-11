#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import time
from util.tool.btask import background_task, TaskService


@background_task("a_background_job")
def hi(name):
    while 1:
        print("hi, {}".format(name))
        time.sleep(1)


if __name__ == '__main__':
    hi("jianbing")

    time.sleep(5)
    TaskService.stop("a_background_job")
    print("stop")
