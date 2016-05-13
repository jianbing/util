#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals, division

import codecs
import hashlib
import os
import subprocess
import sys
import time
import requests

from utils.decorators import retry, windows

"""
公共类库
"""


def d_(astr):
    # print astr
    # import chardet
    # print chardet.detect(astr)
    return astr.decode('gb2312')


def e_(astr):
    return astr.encode('gb2312')


def explain(target, sleep=True):
    """显示帮助信息

    :param target:
    :param sleep:
    :return:
    """
    print type(target)
    print dir(target)
    help(target)
    if sleep:
        sleep_for(999)


def profile_func(code):
    import cProfile
    cProfile.run(code, "prof.txt")
    import pstats
    p = pstats.Stats("prof.txt")
    p.sort_stats("time").print_stats()



def get_file_size(file_path):
    """返回文件大小，单位是字节

    :param file_path:
    :return:
    """
    return os.path.getsize(file_path)


def get_files_by_suffix(path, suffixes=("txt", "xml"), one_layer=True):
    """从path路径下，找出全部指定后缀名的文件，支持1层目录，或者整个目录遍历

    :param path: 根目录
    :param suffixes: 指定查找的文件后缀名
    :param one_layer: 如果为True，只遍历一层目录
    :return:
    """
    file_list = []
    for root, dirs, files in os.walk(path):
        for afile in files:
            file_suffix = os.path.splitext(afile)[1][1:].lower()   # 后缀名
            if file_suffix in suffixes:
                file_list.append(os.path.join(root, afile))
        if one_layer:
            return file_list

    return file_list


@retry(times=5)
def download_file(url, target_file, proxies=None, check_file=False, check_size=1000):
    """下载文件，通过requests库

    :param url: 目标url
    :param target_file:下载到本地的地址
    :param proxies: 代理
    :param check_file: 是否检查已经下载的文件的大小
    :param check_size: 最小文件大小（字节）
    :return:
    """

    print('start to download {0}'.format(url))

    r = requests.get(url, stream=True, proxies=proxies, timeout=5)

    with open(target_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    if check_file:
        if get_file_size(target_file) < check_size:
            raise Exception("fileSize Error")
    print('finish download')


def sleep_for(times):
    time.sleep(times)


def unzip(afile):
    """解压文件，解压到压缩包所在目录的同名文件夹中

    :param afile:压缩包的绝对路径
    :return:
    """
    folder = os.path.splitext(afile)[0]  # 建立和文件同名的文件夹
    if not os.path.exists(folder):
        os.mkdir(folder)
    import zipfile
    zip_file = zipfile.ZipFile(afile, 'r')
    zip_file.extractall(folder)
    zip_file.close()


def java_timestamp_to_py(java_timestamp):
    """把java的时间戳转为python的，并打印出相应的时间

    :param java_timestamp:
    :return:
    """
    py_time = int(java_timestamp/1000)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(py_time)))


def match_file(file1, file2):
    """对比两个文件的md5，看是否一致

    :param file1:
    :param file2:
    :return:
    """

    with open(file1) as file1, open(file2) as file2:

        file1md5 = hashlib.md5()
        for temp in file1.readlines():
            file1md5.update(temp)

        file2md5 = hashlib.md5()
        for temp in file2.readlines():
            file2md5.update(temp)

        return True if file1md5.hexdigest() == file2md5.hexdigest() else False


@retry(times=3)
def get_url_filesize(url, proxies=None):
    """获取下载链接文件的大小，单位是KB

    :param proxies:
    :param url:
    :return:
    """
    r = requests.head(url=url, proxies=proxies, timeout=3.0)

    while r.is_redirect:    # 如果有重定向
        # print 'got'
        # print r.headers['Location']
        r = requests.head(url=r.headers['Location'], proxies=proxies, timeout=3.0)
    # print r.headers
    # print r.headers['Content-Length']
    return int(r.headers['Content-Length'])/1024


def svn_update(path):
    command = r'TortoiseProc.exe /command:update /path:"{0}" /closeonend:0'.format(path).encode('gb2312')
    print command
    execute_cmd(command, True)


def svn_revert(path):
    command = r'TortoiseProc.exe /command:revert /path:"{0}" /closeonend:0'.format(path).encode('gb2312')
    print command
    execute_cmd(command, True)


def wait_to_exit(seconds):
    print ""
    print "{0}秒后自动退出".format(seconds)
    sleep_for(seconds)


def compare_files():
    a = raw_input('file1\n')
    b = raw_input('file2\n')

    command = 'BCompare.exe {0} {1}'.format(a,b)
    print command
    from config.config import CONST_BCOMPARE_DIR
    os.chdir(CONST_BCOMPARE_DIR)
    execute_cmd(command)


def get_screen_scale(x, y):
    """通过屏幕分辨率，返回屏幕比例

    :param x:
    :param y:
    :return:
    """
    scale = int(y)/int(x)
    if scale == 16/9:
        return 16, 9
    elif scale == 4/3:
        return 4, 3
    elif scale == 15/9:
        return 15, 9
    elif scale == 16/10:
        return 16, 10
    else:
        raise Exception("None scale match")


def execute_cmd(cmd, print_result=False, shell=True):
    """执行cmd命令，返回结果

    :param cmd:
    :param print_result: 是否打印，默认False
    :param shell:
    :return: stdout
    """

    stdout, stderr = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()   # wait 如果输出量多，会死锁

    if print_result:
        print stdout
    if stderr:
        print stderr
    result = stdout.splitlines()
    return result
    # return [i for i in stdout.split('\r\n') if i.strip() != '']


def get_root_dir():
    """获取程序入口文件所在的目录

    :return:
    """
    return os.path.dirname(os.path.realpath(sys.argv[0]).decode('gbk'))


def append_root_dir(path):
    return os.path.join(get_root_dir(), path)


@windows
def get_desktop_dir():
    """获取桌面文件夹地址

    :return:
    """
    # return os.path.join(os.path.abspath(os.environ['HOMEPATH']), 'Desktop')
    return os.path.join("C:", os.environ['HOMEPATH'], 'Desktop')


def search_keyword_from_dirs(path, keyword, suffix=("ejs",), one_layer=False):
    files = get_files_by_suffix(path, suffix, one_layer=one_layer)
    for afile in files:
        try:
            with codecs.open(afile, 'r', encoding='utf-8', errors='ignore') as f:

                file_content = f.read()

                position = file_content.find(keyword)
                if position != -1:
                    print("find in {0}".format(afile))
                    print(file_content[position-100:position+100])
                    print("_"*100)

        except Exception as e:
            print(e)
            print afile
            print("#"*100)
            print("_"*100)


@windows
def is_port_used(port=5037, kill=False):
    cmd = 'netstat -ano | findstr {} | findstr  LISTENING'.format(port)
    print cmd
    result = os.popen(e_(cmd)).read()
    print d_(result)

    if result != '':
        try:
            pid = result.split()[-1]

            result = os.popen('tasklist /FI "PID eq {0}'.format(pid)).read()
            print d_(result)

            position = result.rfind('====='.encode())
            program_name = result[position+5:].split()[0]
            print "占用的程序是{}".format(program_name)

            result = os.popen('wmic process where name="{0}" get executablepath'.format(program_name)).read()

            result = result.split()
            print "占用的程序所在位置：{}".format(d_(result[1]))

            cmd = "explorer {0}".format(os.path.dirname(d_(result[1])))
            execute_cmd(e_(cmd))  # 打开所在文件夹

        except Exception as e:
            print e
        finally:
             if kill:
                print os.popen("taskkill /F /PID {0}".format(pid)).read()   # 结束进程

    else:
        print '{}端口没有被占用'.format(port)


def format_timestamp(timestamp=time.time(), fmt='%Y-%m-%d-%H-%M-%S'):
    """时间戳转为指定的文本格式，默认是当前时间

    :param timestamp:
    :param fmt:
        默认不需要填写，默认='%Y-%m-%d-%H-%M-%S'. 可以更改成自己想用的string
        格式. 比如 '%Y.%m.%d.%H.%M.%S'

    """
    return time.strftime(fmt, time.localtime(timestamp))


if __name__ == '__main__':
    # java_timestamp_to_py(1457341845438)
    # print int(time.time())*1000
    # java_timestamp_to_py(1458824031000)
    #
    # is_port_used()
    # input()
    is_port_used(kill=True)
