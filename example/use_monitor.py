#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created by jianbing on 2018-01-17
"""
from util.tool.monitor import monitor
from util.tool.adb import ADB

if __name__ == '__main__':
    monitor.init(ADB(), False, 10, 200, 5, 20, None)
    monitor.start()