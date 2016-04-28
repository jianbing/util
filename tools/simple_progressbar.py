#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals, division
import sys
import time


class SimpleProgressBar(object):

    def __init__(self, target):
        self.__target = target
        self.__len = len(target)
        self.__num = 0

    def __iter__(self):
        self.__iterable = iter(self.__target)
        return self

    def get_process(self):
        return int(self.__num/self.__len*100)

    def next(self):
        value = next(self.__iterable)
        self.__num += 1
        result = "{0}% |{1}|\r".format(self.get_process(), "X" * 10).replace("X", ">", (int(self.get_process() / 10)))
        sys.stdout.write(result)
        sys.stdout.flush()
        return value


if __name__ == "__main__":

    for i in SimpleProgressBar("abcdefghijk"):

        if i == 'f':
            print ''
            print 'find f'
            break



    raw_input()