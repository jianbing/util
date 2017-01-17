#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import re
import os
import sys
import time
import subprocess
from PIL import Image
from utils.common import get_desktop_dir
from utils import logger


AUTO_INSTALL_PATH = r'C:\\Users\\Bing\\Desktop\\apks'

# adb install 安装错误常见列表
errors = {'INSTALL_FAILED_ALREADY_EXISTS': '程序已经存在',
          'INSTALL_DEVICES_NOT_FOUND': '找不到设备',
          'INSTALL_FAILED_DEVICE_OFFLINE': '设备离线',
          'INSTALL_FAILED_INVALID_APK': '无效的APK',
          'INSTALL_FAILED_INVALID_URI': '无效的链接',
          'INSTALL_FAILED_INSUFFICIENT_STORAGE': '没有足够的存储空间',
          'INSTALL_FAILED_DUPLICATE_PACKAGE': '已存在同名程序',
          'INSTALL_FAILED_NO_SHARED_USER': '要求的共享用户不存在',
          'INSTALL_FAILED_UPDATE_INCOMPATIBLE': '版本不能共存',
          'INSTALL_FAILED_SHARED_USER_INCOMPATIBLE': '需求的共享用户签名错误',
          'INSTALL_FAILED_MISSING_SHARED_LIBRARY': '需求的共享库已丢失',
          'INSTALL_FAILED_REPLACE_COULDNT_DELETE': '需求的共享库无效',
          'INSTALL_FAILED_DEXOPT': 'dex优化验证失败',
          'INSTALL_FAILED_DEVICE_NOSPACE': '手机存储空间不足导致apk拷贝失败',
          'INSTALL_FAILED_DEVICE_COPY_FAILED': '文件拷贝失败',
          'INSTALL_FAILED_OLDER_SDK': '系统版本过旧',
          'INSTALL_FAILED_CONFLICTING_PROVIDER': '存在同名的内容提供者',
          'INSTALL_FAILED_NEWER_SDK': '系统版本过新',
          'INSTALL_FAILED_TEST_ONLY': '调用者不被允许测试的测试程序',
          'INSTALL_FAILED_CPU_ABI_INCOMPATIBLE': '包含的本机代码不兼容',
          'CPU_ABIINSTALL_FAILED_MISSING_FEATURE': '使用了一个无效的特性',
          'INSTALL_FAILED_CONTAINER_ERROR': 'SD卡访问失败',
          'INSTALL_FAILED_INVALID_INSTALL_LOCATION': '无效的安装路径',
          'INSTALL_FAILED_MEDIA_UNAVAILABLE': 'SD卡不存在',
          'INSTALL_FAILED_INTERNAL_ERROR': '系统问题导致安装失败',
          'INSTALL_PARSE_FAILED_NO_CERTIFICATES': '文件未通过认证 >> 设置开启未知来源',
          'INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES': '文件认证不一致 >> 先卸载原来的再安装',
          'INSTALL_FAILED_INVALID_ZIP_FILE': '非法的zip文件 >> 先卸载原来的再安装',
          'INSTALL_CANCELED_BY_USER': '需要用户确认才可进行安装',
          'INSTALL_FAILED_VERIFICATION_FAILURE': '验证失败 >> 尝试重启手机',
          'DEFAULT': '未知错误'
          }


class ADB(object):

    def __init__(self, serial=None, adb_remote=None, debug=False):

        self.__serial = serial
        self.__debug = debug
        self.__adb_remote = adb_remote
        self.__adb_name = ""
        self.__findstr = ""
        self.__init()

    def __init(self):

        self.__adb_name = "adb.exe" if os.name == 'nt' else "adb"
        self.__findstr = "findstr" if os.name == 'nt' else "grep"

        if not self.__debug:
            logger.set_level(logging.INFO)

        if self.__adb_remote:

            logger.info(subprocess.check_output("{} connect {}".format(self.__adb_name, self.__adb_remote)))

        devices_info = self.devices()

        logger.debug(devices_info)

        if not devices_info:
            raise Exception("no phone is connecting.")
        if not self.__serial:
            if len(devices_info) > 1:
                logger.error(devices_info)
                raise Exception("more than one devices,you should specify the serialno.")
            else:
                self.__serial = devices_info[0]

    def adb(self, *args):
        """adb命令执行入口

        :param args:
        :return:
        """

        if self.__serial:
            cmd = " ".join([self.__adb_name, '-s', self.__serial] + list(args))
        else:
            cmd = " ".join([self.__adb_name] + list(args))

        stdout, stderr = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        logger.debug("cmd is {}".format(cmd))
        logger.debug("stdout is {}".format(stdout.strip()))

        if stderr:
            logger.error(stderr)

        result = [i.decode() for i in stdout.splitlines()]
        return [i for i in result if i and not i.startswith("* daemon")]  # 过滤掉空的行，以及adb启动消息

    def adb_shell(self, *args):
        """adb shell命令入口

        :param args:
        :return:
        """
        args = ['shell'] + list(args)
        return self.adb(*args)

    def devices(self):
        result = self.adb('devices')
        if len(result) == 1:
            return []
        logger.debug(result)
        return [i.split()[0] for i in result if not i.startswith('List') and not i.startswith("adb")]

    @property
    def screen_resolution(self):
        """手机屏幕分辨率

        :return:
        """
        result = self.adb_shell("wm size")[0]
        result = result[result.find('size: ') + 6:]   # 1080x1800
        result = result.split('x')
        return result

    @property
    def adb_remote(self):
        return self.__adb_remote

    @property
    def version(self):
        """adb 版本信息

        :return:
        """
        return self.adb('version')[0]

    @property
    def serial(self):
        return self.__serial

    @property
    def android_version(self):
        return self.adb_shell('getprop ro.build.version.release')[0]

    @property
    def wlan_ip(self):
        return self.adb_shell('getprop', 'dhcp.wlan0.ipaddress')[0]

    def screenshot(self, screenshot_dir, info):
        """screencap方式截图

        :param screenshot_dir:
        :param info: 附加信息
        :return:
        """
        start_time = time.time()
        print("开始截图...")
        self.adb_shell("screencap -p /sdcard/screenshot.png")
        temp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(start_time))
        filename = '{0}-{1}.png'.format(temp, info)
        self.adb('pull /sdcard/screenshot.png {}\{}'.format(screenshot_dir, filename))
        print('截图已保存')
        return os.path.join(screenshot_dir, filename)

    def screenshot_ex(self, screenshot_dir, info='shot', compress=True, openfile=True):
        """扩展take_screenshot函数，加入是否压缩和是否打开文件

        :param screenshot_dir:
        :param info:
        :param compress:
        :param openfile:
        :return:
        """
        result = self.screenshot(screenshot_dir, info)
        print('result is {0}'.format(os.path.normpath(result)))
        if compress:
            im = Image.open(result)
            im_size = im.size
            im = im.resize((int(im_size[0] / 2), int(im_size[1] / 2)), Image.ANTIALIAS)  # 尺寸减少一半
            # im = im.rotate(270, expand=1)   # 旋转角度是逆时针的，如果没expand，会出现旋转后，部分图像丢失

            new_file = result.replace(r".png", r".jpg")  # 修改格式，减少图片大小
            im.save(new_file)
            os.remove(result)

            if openfile:
                cmd = r"mspaint {0}".format(new_file)   # 用画图工具打开
                os.popen(cmd)

    def get_mem_using(self, package_name):
        """获取内存占用

        :param package_name: app的包名
        :return: 返回Total内存值 eg ['TOTAL', '286783']
        """
        result = self.adb_shell("dumpsys meminfo {}".format(package_name))
        info = re.search('TOTAL\W+\d+', str(result)).group()
        result = ''
        try:
            result = info.split()
        except Exception as e:
            print(info)
            print(e)
        return result

    def get_cpu_using(self, package_name):
        """获取cpu占用

        :param package_name:
        :return:
        """
        cmd = 'dumpsys cpuinfo |{} "{} TOTAL"'.format(self.__findstr, package_name)
        print(cmd)
        result = self.adb_shell(cmd)
        print(result)
        cpu = game_cpu = 0
        try:
            # 只有TOTAL的情况，在应用刚刚启动的时候
            # ['3.6% TOTAL: 2% user + 1.6% kernel + 0% iowait + 0% softirq\r\r\n']
            if(len(result)) == 1:
                cpu = result[0][:result[0].find('%')].strip()
                game_cpu = 0
            else:
                # 54% 1527/com.funsplay.god.uc: 43% user + 10% kernel / faults: 6 minor 从中截取前边的54 应用占用cpu的百分比
                game_cpu = result[0][:result[0].find('%')].strip()
                cpu = result[-1][:result[-1].find('%')].strip()      # cpu总体占用
        except Exception as e:
            print(e)
            print(result)
        return cpu, game_cpu

    def current_package_info(self):
        result = self.adb_shell('dumpsys activity top')
        for line in result:
            if line.strip().startswith('ACTIVITY'):
                return line.split()[1].split('/')

    def current_package_name(self):
        """获取当前运行app包名

        :return:
        """
        return self.current_package_info()[0]

    def current_activity_name(self):
        """获取当前运行activity

        :return:
        """
        return self.current_package_info()[1]

    def pull_file(self, remote, local):
        return self.adb('pull', remote, local)

    def push_file(self, local, remote):
        return self.adb('push', local, remote)

    @staticmethod
    def start_server():
        logger.debug('adb start-server')
        logger.info(os.popen('adb.exe start-server').read())

    @staticmethod
    def kill_server():
        logger.debug('adb kill-server')
        os.popen('adb.exe kill-server')

    @staticmethod
    def get_package_name_from_apk(apk_path):
        """从apk安装包中，获取包名

        :param apk_path: apk文件位置
        :return:从 package: name='com.funsplay.god.anzhi' versionCode='10300' versionName='1.3.0'中截取包名
        """
        result = os.popen("aapt dump badging {0}".format(apk_path)).read()
        return result[15:result.index('\' versionCode')]

    def auto_install(self, path=AUTO_INSTALL_PATH):
        """自动安装指定目录下的全部apk，如果已经存在，则先卸载

        :param path:
        :return:
        """
        if not os.path.exists(path):
            print('目录不存在')
            return
        print("当前连接的手机是：{0}".format(self.__serial))

        for filename in os.listdir(path):
            if os.path.splitext(filename)[1].lower() == '.apk':
                print("发现apk文件：{0}".format(filename))

                apk_path = '{0}\{1}'.format(path, filename)
                package_name = self.get_package_name_from_apk(apk_path)
                print('apk安装包的包名是：{0}'.format(package_name))

                if self.check_install(package_name):
                    print('手机中已经安装了该应用，准备移除')
                    self.uninstall(package_name)
                else:
                    print('手机未安装该应用')

                print("开始安装：{0}".format(os.path.normpath(filename)))
                self.adb('install {}\{}'.format(path, filename))
        print('任务完成')

    def check_install(self, package_name):
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
        result = self.adb_shell("pm path", self.current_package_name())
        apk_path = result[0].strip().replace('package:', '')
        print('apk位置是：{0}'.format(apk_path))
        print('开始导出apk')
        self.adb("pull {0} {1}\{2}".format(apk_path, path, os.path.split(apk_path)[1]))
        print("备份完成")

    def start_monkey(self, pct_touch=100, pct_motion=0, throttle=200, v='-v -v', times=100, logfile=None):

        if pct_touch + pct_motion != 100:
            raise Exception("sum fo action pct should be 100")

        cmd = [
            'monkey',
            '-p {}'.format(self.current_package_name()),
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
        result = self.adb_shell("ps|{} monkey".format(self.__findstr))
        if result:
            pid = result[0].split()[1]
            self.adb_shell('kill', pid)

    @staticmethod
    def raw_cmd(cmd):
        print('开始执行{}'.format(cmd))
        os.system(cmd)
        print('执行完成')

    def start_app(self, component):
        self.adb_shell("am start -n {}".format(component))

    def stop_app(self,package):
        self.adb_shell('am force-stop {}'.format(package))

if __name__ == "__main__":

    a = ADB(debug=True)
    # print(a.current_package_info())
