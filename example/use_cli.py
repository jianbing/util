#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from util.tool.cli import cli

if __name__ == '__main__':

    @cli.add("hello方法")
    def hello():
        print("hello")


    @cli.add("hi方法")
    def hi():
        print("hi")


    cli.run()
