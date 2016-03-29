#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import threading
from utils.android import *


"""
安卓cpu，内存监测
"""


class _MonitorCPUMem(threading.Thread):
    """
    监测当前运行的apk的内存和cpu占用
    """
    def __init__(self, screen_shot=None, shot_delay=None, min_mem=None, check_delay=None, mem_incr=None,
                 screenshot_dir=None):
        super(_MonitorCPUMem, self).__init__()
        self.__screen_shot = screen_shot
        self.__shot_delay = shot_delay
        self.__min_mem = min_mem
        self.__check_delay = check_delay
        self.__mem_incr = mem_incr
        self.__screenshot_dir = screenshot_dir
        self.__running = False
        self.__mem_date = dict()

    def is_running(self):
        return self.__running

    def shut_down(self):
        self.__running = False
        print 'Shutdown Monitor'
        self.analyse()

    def init(self, screen_shot=False, shot_delay=10, min_mem=200, check_delay=3, mem_incr=20,
             screenshot_dir=None):
        """初始化

        :param screen_shot: 是否截图
        :param shot_delay: 每次截图间隔，建议大于10s
        :param min_mem: 最低截图内存
        :param check_delay: 每次监测检测，建议大于5s
        :param mem_incr: 新截图需要当前内存大于之前内存mem_incr mb
        :param screenshot_dir: 截图目录
        :return:
        """
        self.__screen_shot = screen_shot
        self.__shot_delay = shot_delay
        self.__min_mem = min_mem
        self.__check_delay = check_delay
        self.__mem_incr = mem_incr
        self.__screenshot_dir = screenshot_dir

    def run(self):
        self.__running = True
        print 'Running Monitor'
        info = get_activity_info()
        if not info:
            print '没有发现手机'
            return

        print 'APK is {0}'.format(info[0])
        last_shot_mem = 0
        last_shot_time = 0
        while True:
            if not self.__running:
                break
            mem_now = get_mem_info(info[2], info[0])
            mem_now = int(mem_now[1])
            cpu_use = get_cpu_info(info[2], info[0])   # cpu, game_cpu
            current_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
            print current_time
            print "APK占用CPU：{0}%，当前CPU总占用{1}%".format(float(cpu_use[0])*float(cpu_use[1])/100, cpu_use[0])
            print "MEM占用：{0}MB".format(int(mem_now/1024))

            self.__mem_date[current_time] = int(mem_now / 1024)   # 收集内存数据

            if self.__screen_shot:
                if mem_now - last_shot_mem > self.__mem_incr*1024:
                    if (time.time()-last_shot_time) > self.__shot_delay:
                        last_shot_mem = mem_now
                        last_shot_time = time.time()

                        take_screenshot(self.__screenshot_dir, 'shot')
                    else:
                        print "距离上次截图间隔不足{0}秒".format(self.__shot_delay)
            time.sleep(self.__check_delay)

    def analyse(self):
        print '检测期间最高内存占用是：{0}MB'.format(max(self.__mem_date.values()))


monitor = _MonitorCPUMem()


def get_new_monitor():
    global monitor
    monitor = _MonitorCPUMem()
    return monitor
