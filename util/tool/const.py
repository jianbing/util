#! /usr/bin/env python
# -*- coding: UTF-8 -*-


class Const(object):
    def __setattr__(self, key, value):
        if not key.isupper():
            raise Exception('Const value should be upper')
        if key in self.__dict__:
            raise Exception('Const value cannot be changed')
        self.__dict__[key] = value


if __name__ == '__main__':
    const = Const()
    const.A = 1
    print(const.A)
    const.A = 2
