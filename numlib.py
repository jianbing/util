#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import re
"""
测试数值的各种辅助函数
"""


def format_msec(msec):
    """把毫秒数转化为1d5h33m50s的形式，如1077508000 --> 12d11h18m28s

    :param msec:
    :return:
    """
    data = int(msec) / 1000
    day_num = data / (3600 * 24)

    data %= 3600 * 24
    hour_num = data / 3600

    data %= 3600
    min_num = data / 60
    sec_num = data % 60

    nums = [day_num, hour_num, min_num, sec_num]
    words = ['d', 'h', 'm', 's']
    start_print = False
    result = list()
    for num, word in zip(nums, words):
        if num > 0:
            start_print = True
        if start_print:
            result.append(str(num))
            result.append(word)
    return ''.join(result)


def count_digit_number(astr, print_num=False):
    """统计字符串里边，数字的数量

    :param astr:
    :param print_num:
    :return:
    """
    result = re.findall("\d+", astr)
    if print_num:
        for i in result:
            print(i)
    print("数字数量是{}个".format(len(result)))


if __name__ == '__main__':
    pass
