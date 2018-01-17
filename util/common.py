#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import hashlib
import subprocess
import zipfile
import requests
from util.decorator import *
from util.tool.file import File


def remove_bom(file_path):
    """移除utf-8文件的bom字节

    :param file_path:
    :return:
    """
    ''''''
    bom = b'\xef\xbb\xbf'
    exist_bom = lambda s: True if s == bom else False

    f = open(file_path, 'rb')
    if exist_bom(f.read(3)):
        body = f.read()
        f.close()
        with open(file_path, 'wb') as f:
            f.write(body)


def is_utf_bom(file_path):
    """判断文件是否是utf-8-bom

    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as f:
        if f.read(3) == b'\xef\xbb\xbf':
            return True
        return False


def run_cmd(cmd, print_result=False, shell=True):
    """执行cmd命令，返回结果

    :param cmd:
    :param print_result: 是否打印，默认False
    :param shell:
    :return: stdout
    """

    stdout, stderr = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).communicate()  # wait 如果输出量多，会死锁

    if print_result:
        print(stdout)

    if stderr:
        print(stderr)
    result = [i.decode('utf-8') for i in stdout.splitlines()]
    return result


def get_local_ip():
    """获取本地ip地址

    :return:
    """
    import socket
    return socket.gethostbyname(socket.gethostname())


@windows
def get_desktop_dir():
    """获取桌面文件夹地址

    :return:
    """
    return os.path.join("C:", os.environ['HOMEPATH'], 'Desktop')


def max_n(a_list, num):
    """从一个列表里边，获取最大的n的值，如果num大于列表内的总数量，则返回整个列表

    :param a_list:
    :param num:
    :return:
    """
    import heapq
    return heapq.nlargest(num, a_list)


def profile_func(call_func_str):
    """分析函数的运行消耗

        def f():
            d = AndroidDevice("192.168.1.120")
            d.swipe_position(650, 700, 50, 700, 30)
            d.swipe_position(130, 800, 850, 800, 50)

        profile_func("f()")

    :param call_func_str:
    :return:
    """
    import cProfile
    cProfile.run(call_func_str, "prof.txt")
    import pstats
    p = pstats.Stats("prof.txt")
    p.sort_stats("time").print_stats()


def get_file_size(file_path):
    """返回文件大小，单位是字节

    :param file_path:
    :return:
    """
    return os.path.getsize(file_path)


def get_files_by_suffix(path, suffixes=("txt", "xml"), traverse=True):
    """从path路径下，找出全部指定后缀名的文件，支持1层目录，或者整个目录遍历

    :param path: 根目录
    :param suffixes: 指定查找的文件后缀名
    :param traverse: 如果为False，只遍历一层目录
    :return:
    """
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_suffix = os.path.splitext(file)[1][1:].lower()  # 后缀名
            if file_suffix in suffixes:
                file_list.append(os.path.join(root, file))
        if not traverse:
            return file_list

    return file_list


def get_files_by_suffix_ex(path: str, suffixes: tuple = ("txt", "xml"), traverse: bool = True):
    """从path路径下，找出全部指定后缀名的文件，支持1层目录，或者整个目录遍历

    :param path: 根目录
    :param suffixes: 指定查找的文件后缀名
    :param traverse: 如果为False，只遍历一层目录
    :return: File对象列表
    """
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_suffix = os.path.splitext(file)[1][1:].lower()  # 后缀名
            if file_suffix in suffixes:
                file_list.append(File(os.path.join(root, file)))
        if not traverse:
            return file_list

    return file_list


def unzip(file_path):
    """解压文件，解压到压缩包所在目录的同名文件夹中

    :param file_path:压缩包的绝对路径
    :return:
    """
    folder = os.path.splitext(file_path)[0]  # 建立和文件同名的文件夹
    if not os.path.exists(folder):
        os.mkdir(folder)
    zip_file = zipfile.ZipFile(file_path, 'r')
    zip_file.extractall(folder)
    zip_file.close()


def format_timestamp(timestamp=time.time(), fmt='%Y-%m-%d-%H-%M-%S'):
    """时间戳转为指定的文本格式，默认是当前时间

    :param timestamp:
    :param fmt: 默认不需要填写，默认='%Y-%m-%d-%H-%M-%S'. 可以更改成自己想用的string格式. 比如 '%Y.%m.%d.%H.%M.%S'

    """
    return time.strftime(fmt, time.localtime(timestamp))


def is_chinese(unicode_text):
    """检测unicode文本是否为中文

    :param unicode_text:
    :return:
    """
    for uchar in unicode_text:
        if uchar >= '\u4e00' and not uchar > '\u9fa5':
            return True
    else:
        return False


def java_timestamp_to_py(java_timestamp):
    """把java的时间戳转为python的，并打印出相应的时间

    :param java_timestamp:
    :return:
    """
    py_time = int(java_timestamp / 1000)
    print((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(py_time))))


def match_file(file1, file2):
    """对比两个文件的md5，看是否一致

    :param file1:
    :param file2:
    :return:
    """

    with open(file1, encoding="utf-8") as file1, open(file2, encoding="utf-8") as file2:

        file1md5 = hashlib.md5()
        for temp in file1.readlines():
            file1md5.update(temp.encode('utf-8'))

        file2md5 = hashlib.md5()
        for temp in file2.readlines():
            file2md5.update(temp.encode('utf-8'))

        return True if file1md5.hexdigest() == file2md5.hexdigest() else False


@retry(times=3)
def get_url_file_size(url, proxies=None):
    """获取下载链接文件的大小，单位是KB

    :param proxies:
    :param url:
    :return:
    """
    r = requests.head(url=url, proxies=proxies, timeout=3.0)

    while r.is_redirect:  # 如果有重定向
        r = requests.head(url=r.headers['Location'], proxies=proxies, timeout=3.0)
    return int(r.headers['Content-Length']) / 1024


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
        for chunk in r.iter_content(chunk_size=2048):
            f.write(chunk)
    if check_file:
        if get_file_size(target_file) < check_size:
            raise Exception("fileSize Error")
    print('finish download')


@windows
def is_port_used(port=5037, kill=False):
    cmd = 'netstat -ano | findstr {} | findstr  LISTENING'.format(port)
    print(cmd)
    result = os.popen(cmd).read()
    print(result)
    pid = None
    if result != '':
        try:
            pid = result.split()[-1]

            result = os.popen('tasklist /FI "PID eq {0}'.format(pid)).read()
            """:type: str """
            print(result)

            position = result.rfind('=====')
            program_name = result[position + 5:].split()[0]
            print("占用的程序是{}".format(program_name))

            result = os.popen('wmic process where name="{0}" get executablepath'.format(program_name)).read()

            result = result.split()
            print("占用的程序所在位置：{}".format(result[1]))

            cmd = "explorer {0}".format(os.path.dirname(result[1]))
            run_cmd(cmd)  # 打开所在文件夹

        except Exception:
            import traceback
            traceback.print_exc()
        finally:
            if kill:
                if not pid:
                    raise Exception("pid is None")
                print(os.popen("taskkill /F /PID {0}".format(pid)).read())  # 结束进程

    else:
        print('{}端口没有被占用'.format(port))


def get_screen_scale(x: int, y: int):
    """通过屏幕分辨率，返回屏幕比例

    :param x:
    :param y:
    :return:
    """
    x = int(x)
    y = int(y)
    scale = x / y
    if scale == 16 / 9:
        return 16, 9
    elif scale == 4 / 3:
        return 4, 3
    elif scale == 15 / 9:
        return 15, 9
    elif scale == 16 / 10:
        return 16, 10
    else:
        def gcd(a, b):
            if b == 0:
                return a
            else:
                return gcd(b, a % b)

        scale = gcd(x, y)
        print("没有找到合适的比例")
        return x / scale, y / scale


def search_keyword_from_dirs(path, keyword, suffix=("txt", "xml"), traverse=True, length=100):
    files = get_files_by_suffix(path, suffix, traverse=traverse)
    print("发现{}个文件".format(len(files)))
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:

                content = f.read().lower()
                position = content.find(keyword.lower())

                if position != -1:
                    print("Find in {0}".format(file))
                    start = position - length if position - length > 0 else 0
                    end = position + length if position + length < len(content) else len(content)
                    print(content[start:end])
                    print("_" * 100)

        except Exception as e:
            print(e)
            print(file)
            print(("#" * 100))
            print(("_" * 100))


if __name__ == '__main__':
    print(get_screen_scale(1280, 720))
