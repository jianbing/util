#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import abc
from collections import OrderedDict


class Cmd(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, title, hotkey=None, cmd_help=None):
        self.__title = title
        self.__hotkey = hotkey
        self.__cmd_help = cmd_help

    @abc.abstractmethod
    def run(self):
        pass

    @property
    def hotkey(self):
        return self.__hotkey

    @property
    def title(self):
        return self.__title


class __CmdCenter(object):

    def __init__(self):
        self.cmds = OrderedDict()
        self.cmds_hotkey = dict()

    def add_cmd(self, cmd):
        self.cmds[str(len(self.cmds) + 1)] = cmd

        if cmd.hotkey:
            if cmd.hotkey in self.cmds_hotkey:
                print "\n热键冲突,{0}和{1}".format(cmd.title, self.cmds_hotkey[cmd.hotkey].title)
            else:
                self.cmds_hotkey[cmd.hotkey] = cmd

    def show_cmds(self):
        for key in self.cmds:
            print '{0}，{1}'.format(key, self.cmds[key].title)

    def get_choice(self):
        choice = raw_input("请选择\n".encode('gb2312'))
        return choice

    def work(self):
        while True:
            try:
                print '-'*90
                print '请选择指令'
                print ''
                self.show_cmds()

                while True:
                    choice = self.get_choice()
                    if choice not in self.cmds and choice not in self.cmds_hotkey:
                        print '选择错误，重新选择'
                        continue
                    break

                print ''

                if choice in self.cmds:
                    self.cmds[choice].run()
                else:
                    self.cmds_hotkey[choice].run()
                print ''
                print '执行完成'
                print ''
            except KeyboardInterrupt:
                print '手动退出'

CmdCenter = __CmdCenter()








