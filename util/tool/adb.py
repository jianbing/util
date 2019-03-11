#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
import subprocess
import time
import traceback
from contextlib import contextmanager
from PIL import Image
from util.decorator import windows
from util.tool import log
from util.common import run_cmd, is_chinese, get_desktop_dir
from functools import lru_cache


@windows
class ADB:
    def __init__(self, serial=None, adb_remote=None, chdir=""):

        self._serial = serial
        self._adb_remote = adb_remote
        self._adb_name = "adb.exe"
        self._findstr = "findstr"
        self._chidr = chdir

        self._func_data = dict()  # 存储各函数运行时的临时数据
        self._init_adb()

    @contextmanager
    def _change_dir(self):
        cwd_backup = os.getcwd()
        if self._chidr:
            os.chdir(self._chidr)
        yield
        os.chdir(cwd_backup)

    def _init_adb(self):

        if self._adb_remote:
            with self._change_dir():
                log.info(subprocess.check_output("{} connect {}".format(self._adb_name, self._adb_remote)))

        if not self._serial:
            devices_info = self.devices()
            log.debug(devices_info)

            if not devices_info:
                raise Exception("当前没有已连接的安卓设备")
            if len(devices_info) > 1:
                log.error(devices_info)
                print("当前通过数据线连接的安卓设备有")
                for i in devices_info:
                    print(i)
                print("")
                raise Exception("同时有多个安卓设备连接着电脑，需要指定serialno.")
            else:
                self._serial = devices_info[0]

            # get_app_cpu_using 使用
            self._func_data['cpu_cost'] = None
            self._func_data['cpu_cost_update_time'] = None

    def is_connect(self):
        return self.serial in self.devices()

    def adb(self, *args):
        """adb命令执行入口

        :param args:
        :return:
        """

        if self._serial:
            cmd = " ".join([self._adb_name, '-s', self._serial] + list(args))
        else:
            cmd = " ".join([self._adb_name] + list(args))
        with self._change_dir():
            stdout, stderr = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE).communicate()
        log.debug("cmd is {}".format(cmd))
        log.debug("stdout is {}".format(stdout.strip()))
        log.debug("stderr is {}".format(stderr.decode('gbk')))
        result = [i.decode() for i in stdout.splitlines()]
        return [i for i in result if i and not i.startswith("* daemon")]  # 过滤掉空的行，以及adb启动消息

    def adb_shell(self, *args):
        """adb shell命令入口

        :param args:
        :return:
        """
        args = ['shell'] + list(args)
        return self.adb(*args)

    def tap(self, x, y):
        self.adb_shell("input tap {} {}".format(x, y))

    def swipe(self, sx, sy, ex, ey, steps=100):
        self.adb_shell("input swipe {} {} {} {} {}".format(sx, sy, ex, ey, steps))

    def long_press(self, x, y, steps=1000):
        self.adb_shell("input swipe {} {} {} {} {}".format(x, y, x, y, steps))

    def devices(self):
        result = self.adb('devices')
        if len(result) == 1:
            return []
        log.debug(result)
        return [i.split()[0] for i in result if not i.startswith('List') and not i.startswith("adb")]

    @property
    @lru_cache()
    def resolution(self):
        """手机屏幕分辨率

        :return:
        """
        result = self.adb_shell("wm size")[0]
        result = result[result.find('size: ') + 6:]  # 1080x1800
        result = result.split('x')
        return [int(i) for i in result]

    @property
    @lru_cache()
    def orientation(self):
        for i in self.adb_shell('dumpsys', 'display'):
            index = i.find("orientation")
            if index != -1:
                return int(i[index + 12:index + 13])
        raise Exception("找不到orientation")

    @property
    def adb_remote(self):
        return self._adb_remote

    @property
    @lru_cache()
    def version(self):
        """adb 版本信息

        :return:
        """
        return self.adb('version')[0]

    @property
    def serial(self):
        return self._serial

    @property
    def android_version(self):
        return self.adb_shell('getprop ro.build.version.release')[0]

    @property
    def wlan_ip(self):
        """获取IP地址，基于 adb shell ifconfig

        :return:
        """
        for i in self.adb_shell('ifconfig'):
            i = i.strip()
            if i.startswith("inet addr") and i.find("Bcast") != -1:
                return i[i.find("inet addr:") + len("inet addr:"): i.find("Bcast")].strip()

    def screenshot(self, screenshot_dir, info="N"):
        """screencap方式截图

        :param screenshot_dir:
        :param info: 附加信息
        :return:
        """
        start_time = time.time()
        print("开始截图...")
        self.adb_shell("screencap -p /sdcard/screenshot.png")
        filename = '{0}-{1}.png'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(start_time)), info)
        self.adb('pull /sdcard/screenshot.png {}\{}'.format(screenshot_dir, filename))
        print('截图已保存')
        return os.path.join(screenshot_dir, filename)

    def screenshot_ex(self, screenshot_dir, info='shot', compress=(0.5, 0.5)):
        """扩展screenshot函数，加入是否压缩和是否打开文件

        :param screenshot_dir:
        :param info:
        :param compress:
        :return:
        """
        png_file = self.screenshot(screenshot_dir, info)
        print('screenshot is {0}'.format(os.path.normpath(png_file)))
        if compress:
            im = Image.open(png_file)
            im_size = im.size
            im = im.resize((int(im_size[0] * compress[0]), int(im_size[1] * compress[1])), Image.ANTIALIAS)  # 尺寸减少一半
            # im = im.rotate(270, expand=1)   # 旋转角度是逆时针的，如果没expand，会出现旋转后，部分图像丢失

            compress_file = png_file.replace(r".png", r"_small.png")
            im.save(compress_file)
            return compress_file

    def screenshot_by_minicap(self, screenshot_dir, file_name="", scale=1.0):

        start_time = time.time()
        w, h = self.resolution
        r = self.orientation
        params = '{x}x{y}@{rx}x{ry}/{r}'.format(x=w, y=h, rx=int(w * scale), ry=int(h * scale), r=r * 90)
        self.adb_shell(
            '"LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -s -P {} > /sdcard/minicap-screenshot.jpg"'.format(
                params))
        if not file_name:
            file_name = '{0}.jpg'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(start_time)))
        self.adb('pull /sdcard/minicap-screenshot.jpg {}\{}'.format(screenshot_dir, file_name))

    def get_app_mem_using(self, package_name=None):
        """获取内存占用

        :param package_name: app的包名
        :return: 返回app的内存总占用，单位MB
        """
        try:
            if not package_name:
                package_name = self.current_package_name
                log.debug(package_name)
            result = self.adb_shell("dumpsys meminfo {}".format(package_name))
            info = re.search('TOTAL\W+\d+', str(result)).group()
            result = info.split()
            return int(int(result[-1]) / 1000)
        except:
            import traceback
            traceback.print_exc()
            return 0

    def get_total_cpu_using(self):
        """获取手机当前CPU的总占用，不太准确，延迟很大

        :return:
        """

        cmd = 'dumpsys cpuinfo |{} "TOTAL"'.format(self._findstr)
        result = self.adb_shell(cmd)
        assert len(result) == 1
        result = result[0]
        cpu = 0
        try:
            cpu = float(result[:result.find('%')].strip())
        except:
            print(result)
        return cpu

    def get_app_cpu_using(self, pid=None):
        """采集当前运行的app的CPU占用，首次调用会延迟一秒统计出数据再返回

        :param pid:
        :return:
        """

        if not pid:
            pid = self.current_pid
        cmd = 'cat /proc/{}/stat'.format(pid)
        now = time.time()
        try:
            cpu = sum([int(i) for i in self.adb_shell(cmd)[0].split()[13:17]])

            if not self._func_data['cpu_cost']:
                self._func_data['cpu_cost'] = cpu
                self._func_data['cpu_cost_update_time'] = now
                time.sleep(1)
                return self.get_app_cpu_using(pid)
            else:
                cpu_use = cpu - self._func_data['cpu_cost']
                self._func_data['cpu_cost'] = cpu
                self._func_data['cpu_cost_update_time'] = now
                result = float("{:.2f}".format(cpu_use / (now - self._func_data['cpu_cost_update_time']) / 10))

                if result < 0:
                    log.error("采集到的CPU占用数据异常：{}".format(result))
                    return 0
                return result
        except:
            traceback.print_exc()
            return 0

    @property
    def current_package_info(self):
        result = self.adb_shell('dumpsys activity activities | {} mResumedActivity'.format(self._findstr))
        assert len(result) == 1, result
        return result[0].split()[-2].split("/")

    @property
    @lru_cache()
    def current_pid(self):
        result = self.adb_shell("ps|{} {}".format(self._findstr, self.current_package_name))
        log.info(result)
        return result[0].split()[1]

    @property
    def current_package_name(self):
        """获取当前运行app包名

        :return:
        """
        return self.current_package_info[0]

    @property
    def current_activity_name(self):
        """获取当前运行activity

        :return:
        """
        return self.current_package_info[1]

    def pull_file(self, remote, local):
        """从手机导出文件到本地 eg  pull_file("/sdcard/screenshot.png", "1.png")

        :param remote:
        :param local:
        :return:
        """
        return self.adb('pull', remote, local)

    def push_file(self, local, remote):
        """上传文件到手机

        :param local:
        :param remote:
        :return:
        """
        return self.adb('push', local, remote)

    @staticmethod
    def start_server():
        log.debug('adb start-server')
        log.info(os.popen('adb.exe start-server').read())

    @staticmethod
    def kill_server():
        log.debug('adb kill-server')
        os.popen('adb.exe kill-server')

    @staticmethod
    def get_package_name_from_apk(apk_path):
        """从apk安装包中，获取包名

        :param apk_path: apk文件位置
        :return:
        """
        return ADB.get_apk_info_from_apk_file(apk_path)[0]

    @staticmethod
    def get_apk_info_from_apk_file(apk_path):
        """从apk安装包中，获取包名，和版本信息

        :param apk_path: apk文件位置
        :return:从 package: name='com.funsplay.god.anzhi' versionCode='10300' versionName='1.3.0' 中获取信息
        """
        result = "\n".join(run_cmd('aapt dump badging "{0}"'.format(apk_path)))
        package_name = result[result.index("name=\'") + 6:result.index("\' versionCode")]
        version_code = result[result.index("versionCode=\'") + 13:result.index("\' versionName")]
        version_name = result[result.index("versionName=\'") + 13:result.index("\' platformBuildVersionName")]
        return package_name, version_code, version_name

    def auto_install(self, path):
        """path可以是目录，自动安装目录下的全部apk，如果已经存在，则先卸载
           path也可以是具体apk路径

        :param path:
        :return:
        """
        if not os.path.exists(path):
            print('不存在的路径：{}'.format(path))
            return

        if os.path.isdir(path):
            print("当前连接的手机是：{0}".format(self._serial))
            for filename in os.listdir(path):
                if os.path.splitext(filename)[1].lower() == '.apk':
                    self.install(os.path.join(path, filename))
        else:
            if os.path.splitext(path)[1].lower() == '.apk':
                self.install(path)
            else:
                print("文件后缀名不是apk")

        print('任务完成')

    def install(self, apk_path):
        print("发现apk文件：{0}".format(apk_path))
        dir_path, filename = os.path.split(apk_path)
        rename = False
        raw_apk_path = apk_path
        if is_chinese(filename):
            print("apk文件名存在中文，进行重命名")
            new_apk_path = os.path.join(dir_path, "{}.apk".format(int(time.time())))
            os.rename(raw_apk_path, new_apk_path)
            apk_path = new_apk_path
            rename = True

        package_name = self.get_package_name_from_apk(apk_path)
        print('apk安装包的包名是：{0}'.format(package_name))

        if self.is_install(package_name):
            print('手机中已经安装了该应用，准备移除')
            self.uninstall(package_name)
        else:
            print('手机未安装该应用')

        print("开始安装：{0}".format(apk_path))
        self.adb('install {}'.format(apk_path))

        if rename:
            os.rename(apk_path, raw_apk_path)

    def is_install(self, package_name):
        """检查手机中是否已经安装了某个apk

        :param package_name: 应用的包名
        :return:
        """
        return 'package:{0}'.format(package_name) in self.adb_shell("pm list package")

    def uninstall(self, package_name):
        """卸载apk

        :param package_name:
        :return:
        """
        self.adb("uninstall", package_name)

    def backup_current_apk(self, path=get_desktop_dir()):
        """导出当前正在运行的apk到指定目录，默认是桌面

        :param path:导出目录
        :return:
        """
        result = self.adb_shell("pm path", self.current_package_name)
        apk_path = result[0].strip().replace('package:', '')
        print('apk位置是：{0}'.format(apk_path))
        print('开始导出apk')
        apk_name = "{}{}.apk".format(self.current_package_name,
                                     time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())))
        self.adb("pull {0} {1}\{2}".format(apk_path, path, apk_name))
        print("备份完成")

    def start_monkey(self, pct_touch=100, pct_motion=0, throttle=200, v='-v -v', times=100, logfile=None):

        if pct_touch + pct_motion != 100:
            raise Exception("Monkey各行为的配比总和超过了100")

        cmd = [
            'monkey',
            '-p {}'.format(self.current_package_name),
            '--pct-touch {}'.format(pct_touch),
            '--pct-motion {}'.format(pct_motion),
            '--throttle {}'.format(throttle),
            '{}'.format(v),
            '{}'.format(times)
        ]

        if logfile:
            cmd.append(r'> {}'.format(logfile))

        self.adb_shell(*iter(cmd))

    def stop_monkey(self):
        result = self.adb_shell("ps|{} monkey".format(self._findstr))
        if result:
            pid = result[0].split()[1]
            self.adb_shell('kill', pid)

    @staticmethod
    def raw_cmd(cmd):
        print('开始执行{}'.format(cmd))
        os.system(cmd)
        print('执行完成')

    def start_app(self, component):
        log.info(self.adb_shell("am start -n {}".format(component)))

    def stop_app(self, package):
        log.info(self.adb_shell('am force-stop {}'.format(package)))
