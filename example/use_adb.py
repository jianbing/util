#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from util.tool.adb import ADB
from util import log
from util.log.loglevel import LogLevel

if __name__ == '__main__':

    log.set_level(LogLevel.INFO)

    adb = ADB()
    print(adb.android_version)
    print(adb.current_package_info)
    print(adb.screen_resolution)
