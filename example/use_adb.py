#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from util.tool.adb import ADB
from util.tool import log

if __name__ == '__main__':

    log.set_level_to_info()

    adb = ADB()
    print(adb.android_version)
    print(adb.current_package_info)
    print(adb.resolution)
