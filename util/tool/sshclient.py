#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import paramiko
import time
import os
from util import log


class SSHClient(object):

    def __init__(self, host, port, user, pwd):

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=host, port=port, username=user, password=pwd)
        self.sftp = self.ssh.open_sftp()
        """:type: paramiko.sftp_client.SFTPClient"""

    def _get_files_recursion(self, remote_dir, result=[]):
        """递归方式获取指定目录下的全部文件

        :param remote_dir:
        :param result:
        :return:
        """
        if not remote_dir.endswith('/'):
            remote_dir = '{0}/'.format(remote_dir)
        for i in self.sftp.listdir(remote_dir):
            if i.find('.') != -1:
                result.append("{0}{1}".format(remote_dir, i))
            else:
                self._get_files_recursion("{0}{1}/".format(remote_dir, i))
        return result

    def _get_files_yield(self, remote_dir):
        """生成器方式获取指定目录下的全部文件

        :param remote_dir:
        :return:
        """
        if not remote_dir.endswith('/'):
            remote_dir = '{0}/'.format(remote_dir)
        for i in self.sftp.listdir(remote_dir):
            if i.find('.') != -1:
                yield ("{0}{1}".format(remote_dir, i))
            else:
                yield from self._get_files_yield("{0}{1}/".format(remote_dir, i))

    def download_file(self, remote_path, remote_dir, local_dir):

        local_path = os.path.abspath(remote_path.replace(remote_dir, local_dir))
        dirname = os.path.dirname(local_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        self.sftp.get(remote_path, local_path)

    def download_dir(self, remote_dir, local_dir):
        for remote_path in self._get_files_recursion(remote_dir):
            log.debug('start to download {0}'.format(remote_path))
            self.download_file(remote_path, remote_dir, local_dir)

    def upload_file(self, local_file, remote_file):
        self.sftp.put(local_file, remote_file)

    def get_file_update_time(self, path):
        result = self.sftp.listdir_attr(path)
        update_time = set([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.st_mtime)) for i in result])
        if len(update_time) > 1:
            print("配置表更新时间不一致")
            for i in result:
                print("{:<30}更新时间是：{}".format(i.filename, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.st_mtime))))
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[0].st_mtime))

    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        for line in stdout.read().splitlines():
            print(line)
        for line in stderr.read().splitlines():
            print(("command error ---{0}".format(line)))
        print("finish cmd")

    def close(self):
        self.sftp.close()
        self.ssh.close()
