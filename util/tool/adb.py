#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created by jianbing on 2017-11-06
"""
import os
import re
import subprocess
import time
from PIL import Image
from util import log
from util.common import run_cmd, is_chinese, get_desktop_dir

AUTO_INSTALL_PATH = r'C:\\Users\\Bing\\Desktop\\apks'
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


class KeyCode:
    KEYCODE_CALL = 5  # 拨号键
    KEYCODE_ENDCALL = 6  # 挂机键
    KEYCODE_HOME = 3  # Home键
    KEYCODE_MENU = 82  # 菜单键
    KEYCODE_BACK = 4  # 返回键
    KEYCODE_SEARCH = 84  # 搜索键
    KEYCODE_CAMERA = 27  # 拍照键
    KEYCODE_FOCUS = 80  # 对焦键
    KEYCODE_POWER = 26  # 电源键
    KEYCODE_NOTIFICATION = 83  # 通知键
    KEYCODE_MUTE = 91  # 话筒静音键
    KEYCODE_VOLUME_MUTE = 164  # 扬声器静音键
    KEYCODE_VOLUME_UP = 24  # 音量+键
    KEYCODE_VOLUME_DOWN = 25  # 音量-键
    KEYCODE_ENTER = 66  # 回车键
    KEYCODE_ESCAPE = 111  # ESC键
    KEYCODE_DPAD_CENTER = 23  # 导航键 >> 确定键
    KEYCODE_DPAD_UP = 19  # 导航键 >> 向上
    KEYCODE_DPAD_DOWN = 20  # 导航键 >> 向下
    KEYCODE_DPAD_LEFT = 21  # 导航键 >> 向左
    KEYCODE_DPAD_RIGHT = 22  # 导航键 >> 向右
    KEYCODE_MOVE_HOME = 122  # 光标移动到开始键
    KEYCODE_MOVE_END = 123  # 光标移动到末尾键
    KEYCODE_PAGE_UP = 92  # 向上翻页键
    KEYCODE_PAGE_DOWN = 93  # 向下翻页键
    KEYCODE_DEL = 67  # 退格键
    KEYCODE_FORWARD_DEL = 112  # 删除键
    KEYCODE_INSERT = 124  # 插入键
    KEYCODE_TAB = 61  # Tab键
    KEYCODE_NUM_LOCK = 143  # 小键盘锁
    KEYCODE_CAPS_LOCK = 115  # 大写锁定键
    KEYCODE_BREAK = 121  # Break / Pause键
    KEYCODE_SCROLL_LOCK = 116  # 滚动锁定键
    KEYCODE_ZOOM_IN = 168  # 放大键
    KEYCODE_ZOOM_OUT = 169  # 缩小键
    KEYCODE_0 = 7
    KEYCODE_1 = 8
    KEYCODE_2 = 9
    KEYCODE_3 = 10
    KEYCODE_4 = 11
    KEYCODE_5 = 12
    KEYCODE_6 = 13
    KEYCODE_7 = 14
    KEYCODE_8 = 15
    KEYCODE_9 = 16
    KEYCODE_A = 29
    KEYCODE_B = 30
    KEYCODE_C = 31
    KEYCODE_D = 32
    KEYCODE_E = 33
    KEYCODE_F = 34
    KEYCODE_G = 35
    KEYCODE_H = 36
    KEYCODE_I = 37
    KEYCODE_J = 38
    KEYCODE_K = 39
    KEYCODE_L = 40
    KEYCODE_M = 41
    KEYCODE_N = 42
    KEYCODE_O = 43
    KEYCODE_P = 44
    KEYCODE_Q = 45
    KEYCODE_R = 46
    KEYCODE_S = 47
    KEYCODE_T = 48
    KEYCODE_U = 49
    KEYCODE_V = 50
    KEYCODE_W = 51
    KEYCODE_X = 52
    KEYCODE_Y = 53
    KEYCODE_Z = 54
    KEYCODE_PLUS = 81  # +
    KEYCODE_MINUS = 69  # -
    KEYCODE_STAR = 17  # *
    KEYCODE_SLASH = 76  # /
    KEYCODE_EQUALS = 70  # =
    KEYCODE_AT = 77  # @
    KEYCODE_POUND = 18  # #
    KEYCODE_APOSTROPHE = 75  # '
    KEYCODE_BACKSLASH = 73  # \
    KEYCODE_COMMA = 55  # ,
    KEYCODE_PERIOD = 56  # .
    KEYCODE_LEFT_BRACKET = 71  # [
    KEYCODE_RIGHT_BRACKET = 72  # ]
    KEYCODE_SEMICOLON = 74  # ;
    KEYCODE_GRAVE = 68  # `
    KEYCODE_SPACE = 62  # 空格键
    KEYCODE_MEDIA_PLAY = 126  # 多媒体键 >> 播放
    KEYCODE_MEDIA_STOP = 86  # 多媒体键 >> 停止
    KEYCODE_MEDIA_PAUSE = 127  # 多媒体键 >> 暂停
    KEYCODE_MEDIA_PLAY_PAUSE = 85  # 多媒体键 >> 播放 / 暂停
    KEYCODE_MEDIA_FAST_FORWARD = 90  # 多媒体键 >> 快进
    KEYCODE_MEDIA_REWIND = 89  # 多媒体键 >> 快退
    KEYCODE_MEDIA_NEXT = 87  # 多媒体键 >> 下一首
    KEYCODE_MEDIA_PREVIOUS = 88  # 多媒体键 >> 上一首
    KEYCODE_MEDIA_CLOSE = 128  # 多媒体键 >> 关闭
    KEYCODE_MEDIA_EJECT = 129  # 多媒体键 >> 弹出
    KEYCODE_MEDIA_RECORD = 130  # 多媒体键 >> 录音


class ADB:
    def __init__(self, serial=None, adb_remote=None, debug=False):

        self._serial = serial
        self._debug = debug
        self._adb_remote = adb_remote
        self._adb_name = ""
        self._findstr = ""
        self._init_adb()

        self._last_update_cpu_time = None
        self._last_cpu = None

    def _init_adb(self):

        self._adb_name = "adb.exe" if os.name == 'nt' else "adb"
        self._findstr = "findstr" if os.name == 'nt' else "grep"

        if self._adb_remote:
            log.info(subprocess.check_output("{} connect {}".format(self._adb_name, self._adb_remote)))

        if not self._serial:
            devices_info = self.devices()
            log.debug(devices_info)

            if not devices_info:
                raise Exception("no phone is connecting.")
            if len(devices_info) > 1:
                log.error(devices_info)
                print("当前通过数据线连接的手机有：")
                for i in devices_info:
                    print(i)
                print("")
                raise Exception("同时有多个手机连接着电脑，需要指定serialno.")
            else:
                self._serial = devices_info[0]

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

        stdout, stderr = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        # print(cmd)
        log.debug("cmd is {}".format(cmd))
        log.debug("stdout is {}".format(stdout.strip()))

        if stderr:
            log.error(stderr)

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
    def screen_resolution(self):
        """手机屏幕分辨率

        :return:
        """
        result = self.adb_shell("wm size")[0]
        result = result[result.find('size: ') + 6:]  # 1080x1800
        result = result.split('x')
        return result

    @property
    def adb_remote(self):
        return self._adb_remote

    @property
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
                cmd = r"mspaint {0}".format(new_file)  # 用画图工具打开
                os.popen(cmd)

    def get_mem_using(self, package_name=None):
        """获取内存占用

        :param package_name: app的包名
        :return: 返回app的内存总占用，单位MB
        """
        if not package_name:
            package_name = self.current_package_name
        result = self.adb_shell("dumpsys meminfo {}".format(package_name))
        info = re.search('TOTAL\W+\d+', str(result)).group()
        result = ''
        try:
            result = info.split()
        except Exception as e:
            print(info)
            print(e)
        return int(int(result[-1]) / 1000)

    def get_cpu_using(self):
        """获取手机当前CPU的总占用

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

    def get_cpu_using_ex(self):
        cmd = 'cat /proc/{}/stat'.format(self.current_pid)
        time_now = time.time()
        cpu = sum([int(i) for i in self.adb_shell(cmd)[0].split()[13:17]])

        if not self._last_cpu:
            self._last_update_cpu_time = time_now
            self._last_cpu = cpu
            return 0
        else:
            cpu_use = cpu - self._last_cpu
            self._last_cpu = cpu
            result = float("{:.2f}".format(cpu_use / (time_now - self._last_update_cpu_time) / 10))

            self._last_update_cpu_time = time_now

            if result < 0:
                log.warn("采集到的CPU占用数据异常：{}".format(result))
                return 0

            return result

    @property
    def current_package_info(self):
        result = self.adb_shell('dumpsys activity top')
        for line in result:
            if line.strip().startswith('ACTIVITY'):
                return line.split()[1].split('/')

    @property
    def current_pid(self):
        result = self.adb_shell("ps|{} {}".format(self._findstr, self.current_package_name))
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
        return self.adb('pull', remote, local)

    def push_file(self, local, remote):
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

    def auto_install(self, path=AUTO_INSTALL_PATH):
        """path可以是目录，自动安装目录下的全部apk，如果已经存在，则先卸载
           path也可以是具体apk路径

        :param path:
        :return:
        """
        if not os.path.exists(path):
            print('目录或者不存在')
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
            raise Exception("sum fo action pct should be 100")

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
