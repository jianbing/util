#! /usr/bin/env python
# -*- coding: utf-8 -*-


from collections import OrderedDict
from prettytable import PrettyTable
import datetime


class Hotkey:
    Enter = "Enter"


class _Command:
    def __init__(self, func, title, hot_key=None, need_confirm=False):
        self.func = func
        self.title = title
        self.hot_key = hot_key
        self.need_confirm = need_confirm

    def confirm(self):
        if not self.need_confirm:
            return True
        choice = input("输入yes确认执行 {} ：".format(self.title))
        if choice == "yes":
            return True
        print("没有输入yes，确认没有通过")
        return False

    def run(self):
        self.func()


class _CliTool:
    def __init__(self):
        self.cmds = OrderedDict()
        self.hotkeys = dict()

    def add_cmd(self, cmd):
        self.cmds[str(len(self.cmds) + 1)] = cmd

        if cmd.hot_key:
            if cmd.hot_key in self.hotkeys:
                print("\n热键冲突,{}和{}".format(cmd.title, self.hotkeys[cmd.hot_key].title))
            else:
                self.hotkeys[cmd.hot_key] = cmd

    def show_cmds(self):

        table = PrettyTable(["ID", "指令", "热键"])
        table.align["指令"] = "l"  # 左对齐

        for cmd_id in self.cmds:
            if not self.cmds[cmd_id].hot_key:
                hot_key = ''
            else:
                hot_key = self.cmds[cmd_id].hot_key
            table.add_row([cmd_id, self.cmds[cmd_id].title, hot_key])

        print(table)

    def choice_cmd(self):
        while 1:
            cmd_id = input("选择指令：")
            if cmd_id == "":
                cmd_id = Hotkey.Enter
            if cmd_id not in self.cmds and cmd_id not in self.hotkeys:
                print('输入的ID或者热键不存在，请重新选择')
                continue
            break
        return cmd_id

    def run(self):
        while True:
            try:
                self.show_cmds()
                cmd_id = self.choice_cmd()

                if cmd_id in self.cmds:
                    cmd = self.cmds[cmd_id]
                else:
                    cmd = self.hotkeys[cmd_id]

                if not cmd.confirm():
                    continue

                cmd.run()
                print('\n执行完成 {}\n'.format(datetime.datetime.now()))

            except KeyboardInterrupt:
                print('手动退出\n')
            except:
                import traceback
                traceback.print_exc()


class cli:
    _cli_tool = _CliTool()

    @classmethod
    def add(cls, title, hot_key=None, need_confirm=False):
        def wrap(func):
            cls._cli_tool.add_cmd(_Command(func, title, hot_key, need_confirm))

        return wrap

    @classmethod
    def run(cls):
        cls._cli_tool.run()
