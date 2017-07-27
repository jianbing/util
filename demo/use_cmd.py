#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from util.tool.cmd import cmd, CmdTool

if __name__ == '__main__':

    @cmd("hello方法")
    def hello():
        print("hello")


    @cmd("hi方法")
    def hi():
        print("hi")


    CmdTool.work()
