#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import inspect
import logging
import logging.handlers
from colorama import Fore, Style
from util.log.loglevel import LogLevel


class ColorLogger(object):
    logger = logging.getLogger('gj_color_logger')
    logger.setLevel(logging.INFO)
    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger.addHandler(logger_handler)

    @classmethod
    def debug(cls, msg):
        stack = inspect.stack()
        cls.logger.debug("DEBUG " + str(msg) +
                         "    Func:{} Line:{} File:{}".format(stack[2].function, stack[2].lineno,
                                                              os.path.basename(stack[2].filename)) +
                         Style.RESET_ALL)

    @classmethod
    def info(cls, msg):
        stack = inspect.stack()
        cls.logger.info(Fore.GREEN + "INFO " + str(msg) +
                        "    Func:{} Line:{} File:{}".format(stack[2].function, stack[2].lineno,
                                                             os.path.basename(stack[2].filename)) +
                        Style.RESET_ALL)

    @classmethod
    def error(cls, msg):
        stack = inspect.stack()
        cls.logger.error(Fore.RED + "ERROR " + str(msg) +
                         "    Func:{} Line:{} File:{}".format(stack[2].function, stack[2].lineno,
                                                              os.path.basename(stack[2].filename)) +
                         Style.RESET_ALL)

    @classmethod
    def warn(cls, msg):
        stack = inspect.stack()
        cls.logger.warning(Fore.YELLOW + "WARNING " + str(msg) +
                           "    Func:{} Line:{} File:{}".format(stack[2].function, stack[2].lineno,
                                                                os.path.basename(stack[2].filename)) +
                           Style.RESET_ALL)

    @classmethod
    def set_level(cls, level):
        if level not in LogLevel.__dict__.values():
            raise Exception("使用了不存在的日志级别")
        cls.logger.setLevel(level)
