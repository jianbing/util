#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict


class _Cmd(object):

    def __init__(self, func, title, hotkey=None, args=None, cmd_help=None):
        self.__func = func
        self.__title = title
        self.__hotkey = hotkey
        self.__args = args
        self.__cmd_help = cmd_help

    def run(self):
        if self.__args:
            self.__func(*self.__args)
        else:
            self.__func()

    @property
    def hotkey(self):
        return self.__hotkey

    @property
    def title(self):
        return self.__title


class _CmdCenter(object):

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
            print '{0}，{1}，hotkey:{2}'.format(key, self.cmds[key].title, self.cmds[key].hotkey)

    def get_choice(self):
        choice = raw_input("Make a choice\n")
        return choice

    def work(self):
        while True:
            try:
                print '-' * 80
                print '请选择指令\n'
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
                print '\n执行完成\n'
            except KeyboardInterrupt:
                print '手动退出\n'
            except:
                import traceback
                traceback.print_exc()

CmdCenter = _CmdCenter()


def cmdline(title, hotkey=None):
    def _cmdline(func):
        CmdCenter.add_cmd(_Cmd(func, title, hotkey))

        def __cmdline(*args, **kwargs):
            return func(*args, **kwargs)
        return __cmdline
    return _cmdline



