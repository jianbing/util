# -*- coding: UTF-8 -*-
from __future__ import unicode_literals, division
import os
import re
from PIL import Image
from utils.common import *
from utils.decorators import check_adb, run_once


@check_adb
def get_device_name():
    """获取手机名称，通过adb devices

    :return:
    """
    command = "adb devices"
    device_info = execute_cmd(cmd=command)

    return re.findall(r'.+(?=\tdevice)', str(device_info[1]))[0]


def get_screen_resolution():
    """获得手机的分辨率

    :return:
    """
    device_name = get_device_name()
    command = "adb -s {0} shell wm size".format(device_name)
    result = execute_cmd(command)[0].strip()
    result = result[result.find('size: ')+6:]   # 1080x1800
    result = result.split('x')
    return result


def take_screenshot(adir, info):
    """通过adb shell screencap进行，无压缩

    :param adir: 截图目录
    :param info: 附加信息，可以是内存占用等
    :return: 返回生成的截图文件的地址
    """
    device_name = get_device_name()
    start_time = time.time()
    print "开始截图..."
    cmd = r'adb -s {0} shell screencap -p /sdcard/screenshot.png'.format(device_name)
    subprocess.Popen(cmd).wait()

    temp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(start_time))
    filename = '{0}-{1}.png'.format(temp,info)
    cmd = r'adb -s {0} pull /sdcard/screenshot.png {1}\{2}'.format(device_name, adir, filename)
    doing = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    doing.wait()
    print '截图已保存'
    return os.path.join(adir, filename)


def take_screenshot_ex(adir, info='shot', compress=True, fileopen=True):
    """扩展take_screenshot函数，加入是否压缩和是否打开文件

    :param adir:
    :param info:
    :param compress:
    :param fileopen:
    :return:
    """

    result = take_screenshot(adir, info)

    print 'result is {0}'.format(os.path.normpath(result))

    if compress:
        im = Image.open(result)
        im_size = im.size
        im = im.resize((int(im_size[0]/2), int(im_size[1]/2)), Image.ANTIALIAS)  # 尺寸减少一半
        # im = im.rotate(270, expand=1)   # 旋转角度是逆时针的，如果没expand，会出现旋转后，部分图像丢失

        new_file = result.replace(r".png", r".jpg")  # 修改格式，减少图片大小
        im.save(new_file)

        os.remove(result)  # 移除旧的png图片

        if fileopen:
            cmd = r"mspaint {0}".format(new_file)   # 用画图工具打开
            execute_cmd(cmd)


def screenshot_uiauto(adir, info):
    """uiautomator的截图方式

    :param adir:
    :param info:
    :return:
    """
    temp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    filename = '{0}-{1}.png'.format(temp,info)
    filename = os.path.join(adir,filename)
    print filename
    from uiautomator import device as d
    d.screenshot(filename)


def screenshot_minicap(adir, info):
    """使用minicap，会自动根据手机当前方向旋转图片，用来作为bug截图最为合适

    :param adir:
    :param info:
    :return:
    """
    print "开始截图..."
    temp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    filename = '{0}-{1}.png'.format(temp,info)
    filename = os.path.join(adir,filename)
    import atx
    d = atx.connect()
    """ :type: atx.device.AndroidDevice"""

    d.screenshot_method = atx.SCREENSHOT_METHOD_MINICAP
    d.screenshot(filename)
    print 'result is {0}'.format(filename)
    execute_cmd("mspaint {0}".format(filename))


def get_mem_info(device_name, package_name):
    """获取内存占用

    :param device_name: 手机名称
    :param package_name: app名称
    :return: 返回Total内存值 eg ['TOTAL', '286783']
    """
    command = "adb -s {0} shell dumpsys meminfo {1}".format(device_name, package_name)
    doing = subprocess.Popen(command, stdout=subprocess.PIPE)
    doing.wait()
    temp = doing.stdout.readlines()
    astr = str(temp)
    info = re.findall('TOTAL\W+\d+', astr)
    result = ''
    try:
        result = re.split('\W+', str(info[0]))
    except Exception:
        print info
    return result


def get_cpu_info(device_name, package_name):
    """获取cpu占用

    :param device_name:
    :param package_name:
    :return:
    """
    # command = "adb -s {0} shell top -n 1 |findstr {1}".format(device_name,activity_name)   #这个执行起来慢很多
    command = 'adb -s {0} shell dumpsys cpuinfo |findstr "{1} TOTAL"'.format(device_name, package_name)

    result = execute_cmd(command, print_result=False, shell=True)
    cpu = game_cpu = 0
    try:
        # 只有TOTAL的情况，在应用刚刚启动的时候，会是 ['3.6% TOTAL: 2% user + 1.6% kernel + 0% iowait + 0% softirq\r\r\n']

        if(len(result)) == 1:
            cpu = result[0][:result[0].find('%')].strip()
            game_cpu = 0
        else:
            # 54% 1527/com.funsplay.god.uc: 43% user + 10% kernel / faults: 6 minor 从中截取前边的54 应用占用cpu的百分比
            game_cpu = result[0][:result[0].find('%')].strip()

            cpu = result[-2][:result[-2].find('%')].strip()      # cpu总体占用
    except Exception as e:
        print e
        print result
    return cpu, game_cpu


def monkey_test(cmd):
    cmd = cmd.format(get_package_name())
    print cmd
    print '开始进行Monkey测试'
    os.system(cmd)
    # execute_cmd(cmd, shell=True, print_result=True)
    print '完成Monkey测试'


@run_once
def get_adb_devices():
    result = execute_cmd('adb devices')
    return result


def get_activity_info():
    """获取当前打开着的应用的Package，Activity,device名称

    :return:a list. eg ['com.UCMobile', 'com.uc.browser.InnerUCMobile','355BBJHJYVBY']
    """
    device_name = get_device_name()
    command = "adb -s {0} shell dumpsys activity top".format(device_name)
    doing = subprocess.Popen(command, stdout=subprocess.PIPE)
    out = doing.communicate()[0]
    for line in out.splitlines():
        if line.strip().startswith('ACTIVITY'):
            return line.split()[1].split('/') + [device_name]


def get_package_name():
    """获取当前正在运行的apk的package name

    :return:
    """
    return get_activity_info()[0]


def decompiler_apk(path):
    print 'start to decompiler {0}'.format(path)
    command = 'apktool d {0}'.format(path)
    print command
    print os.popen(command).read()
    print "finish decompiler"


def get_package_name_from_apk(apk_path):
    """从apk安装包中，获取包名

    :param apk_path: apk文件位置
    :return:从 package: name='com.funsplay.god.anzhi' versionCode='10300' versionName='1.3.0'中截取包名
    """
    cmd = "aapt dump badging {0}".format(apk_path)
    temp = execute_cmd(cmd)[0]
    return temp[15:temp.index('\' versionCode')]


def auto_install(path=r'C:\\Users\\Bing\\Desktop\\apks'):
    """自动安装指定目录下的全部apk，如果已经存在，则先卸载

    :param path:
    :return:
    """
    if not os.path.exists(path):
        print '目录不存在'
        return

    device_name = get_device_name()
    print "发现手机：{0}\n".format(device_name)

    for filename in os.listdir(path):
        if os.path.splitext(filename)[1].lower() == '.apk':
            print "发现apk文件：{0}".format(filename)

            apk_path = '{0}\{1}'.format(path, filename)
            package_name = get_package_name_from_apk(apk_path)
            print 'apk安装包的包名是：{0}'.format(package_name)

            if check_install(device_name, package_name):
                print '手机中已经安装了该应用，准备移除'
                uninstall(device_name, package_name)
            else:
                print '手机未安装该应用'

            command = r'adb -s {0} install {1}\{2}'.format(device_name, path, filename)
            print "开始安装：{0}......".format(os.path.normpath(filename))
            print command
            print "正在安装中，请稍等"
            execute_cmd(cmd=command, print_result=True)
    print '任务完成'


def check_install(device_name, package_name):
    """检查手机中是否已经安装了某个apk

    :param device_name: 手机名称
    :param package_name: 应用的包名
    :return:
    """
    command = 'adb -s {0} shell pm list package'.format(device_name)
    doing = subprocess.Popen(command, stdout=subprocess.PIPE)
    out = doing.communicate()[0]
    return 'package:{0}'.format(package_name) in out.splitlines()


def uninstall(device_name, package_name):
    """卸载apk

    :param device_name:
    :param package_name:
    :return:
    """
    command = 'adb -s {0} uninstall {1}'.format(device_name, package_name)
    execute_cmd(cmd=command, print_result=True)


def backup_current_apk(path=get_desktop_dir()):
    """导出当前正在运行的apk到指定目录，默认是桌面

    :param path:导出目录
    :return: 返回cmd命令
    """
    command = "adb shell pm path {0}".format(get_activity_info()[0])
    result = execute_cmd(command)
    apk_path = result[0].strip().replace('package:', '')
    print 'apk位置是：{0}'.format(apk_path)
    command = "adb pull {0} {1}\{2}".format(apk_path, path, os.path.split(apk_path)[1])
    # print command
    print '开始导出apk'
    execute_cmd(command, print_result=True)
    print "备份完成\n"
    return command


if __name__ == "__main__":

    def shot():

        resolution = get_screen_resolution()

        command = 'adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1080x1800@1080x1800/90 -s > /data/local/tmp/atx_screen.jpg'

        execute_cmd(command,shell=False)

        cmd = r'adb pull /data/local/tmp/atx_screen.jpg C:\\Users\\Bing\\Desktop\\shot\\shot.jpg'
        doing = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        doing.wait()

    t = time.time()

    shot()

    print time.time()-t

