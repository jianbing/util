#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from util.android.adb import ADB
from util import log
log.set_level(log.LogLevel.INFO)

adb = ADB()
print(adb.android_version)
print(adb.current_package_info)