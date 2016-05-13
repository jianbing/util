#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import subprocess

import paramiko

from base import Cmd
from config.config import *
from utils.common import compare_files,svn_update
from utils.tools.sftpclient import SFTPClient


class GetJavaUpdateTime(Cmd):
    def run(self):
        sftp = SFTPClient(host=CONST_HOST, port=CONST_PORT, user=CONST_USERNAME, pwd=CONST_PWD)
        print '内网发版时间是：'
        print sftp.get_file_update_time(path='/data/www/god/test/socket/conf/config/treasure')
        sftp.close()


class Reboot(Cmd):
    def run(self):
        print '重启内网中\n'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=CONST_HOST, username=CONST_USERNAME, password=CONST_PWD)
        stdin, stdout, stderr = ssh.exec_command("/etc/init.d/sg_dev_game restart")
        for line in stdout.read().splitlines():
            print(line)
        for line in stderr.read().splitlines():
            print("command error ---{0}".format(line))
        stdin.close()


class CompareFiles(Cmd):
    def run(self):
        compare_files()


class CheckTestServerConfig(Cmd):
    def run(self):
        from testtool.cmdtool.pc.check_xml import check_test_server_xml
        check_test_server_xml()


class SVNUpdatePlan(Cmd):
    def run(self):
        # 更新策划文档
        svn_update(CONST_PLAN_DOC)
