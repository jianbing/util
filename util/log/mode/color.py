#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
from util.log.log_level import LogLevel
import sys
import logging.handlers
from colorama import Fore, Style


class ColorLogger(object):
    logger = logging.getLogger('color_logger')
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger.addHandler(logger_handler)

    @classmethod
    def debug(cls, msg):
        cls.logger.debug("DEBUG " + str(msg))

    @classmethod
    def info(cls, msg):
        cls.logger.error(Fore.GREEN + "INFO " + str(msg) + Style.RESET_ALL)

    @classmethod
    def error(cls, msg):
        cls.logger.error(Fore.RED + "ERROR " + str(msg) + Style.RESET_ALL)

    @classmethod
    def warn(cls, msg):
        cls.logger.warning(Fore.YELLOW + "WARNING " + str(msg) + Style.RESET_ALL)

    @classmethod
    def set_level(cls, level):
        if level not in LogLevel.__dict__.values():
            raise Exception("使用了不存在的日志级别")
        cls.logger.setLevel(level)


