#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import sys
from util.log.loglevel import LogLevel


class _Logger(object):

    def __init__(self, name, std, formatter='%(asctime)s %(levelname)s %(message)s'):
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.DEBUG)
        self._log_handler = logging.StreamHandler(std)
        self._log_handler.setFormatter(logging.Formatter(formatter))
        self.log.addHandler(self._log_handler)


class NormalLogger(object):

    logger = _Logger('gj_normal_logger', sys.stdout)

    @classmethod
    def debug(cls, msg):
        cls.logger.log.debug(msg)

    @classmethod
    def info(cls, msg):
        cls.logger.log.info(msg)

    @classmethod
    def error(cls, msg):
        cls.logger.log.error(msg)

    @classmethod
    def warn(cls, msg):
        cls.logger.log.warning(msg)

    @classmethod
    def set_level(cls, level):
        if level not in LogLevel.__dict__.values():
            raise Exception("使用了不存在的日志级别")
        cls.logger.log.setLevel(level)
