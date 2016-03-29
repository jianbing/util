#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import os

from base import Cmd
from utils.android import auto_install,get_device_name, backup_current_apk,get_package_name,take_screenshot_ex


class AutoInstallAPKs(Cmd):
    def run(self):
        auto_install()


class TakeScreenShot(Cmd):
    def run(self):
        device_name = get_device_name()

        print "发现设备：{0}".format(device_name)
        path = r"C:\\Users\\Bing\\Desktop\\GOD"

        take_screenshot_ex(path)


class TakeScreenShotTemp(Cmd):
    def run(self):
        device_name = get_device_name()

        print "发现设备：{0}".format(device_name)
        path = r"C:\\Users\\Bing\\Desktop\\GOD"
        print "开始截图..."

        result = take_screenshot_ex(path, "shot", False, False)

        print 'result is {0}'.format(os.path.normpath(result))


class BackupCurrentApk(Cmd):
    def run(self):
        backup_current_apk()


class GetPackageName(Cmd):
    def run(self):
        package_name = get_package_name()
        print 'package name:{0}'.format(package_name)


class CountCPUMem(Cmd):
    def run(self):
        from utils.tools.android_monitor import monitor
        monitor.init(False, 10, 200, 3, 20, None)
        monitor.start()


class ScreenScale(Cmd):
    def run(self):
        from utils.common import get_screen_scale
        from utils.android import get_screen_resolution
        resolution = get_screen_resolution()
        print "手机屏幕分辨率是{0}x{1}".format(*resolution)
        print "屏幕比例是{0}比{1}".format(*get_screen_scale(*resolution))