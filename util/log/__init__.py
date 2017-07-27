#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from util.log.mode.color import ColorLogger
from util.log.mode.normal import NormalLogger
from util.log.log_level import LogLevel

_logger = ColorLogger


def debug(msg):
    _logger.debug(msg)


def info(msg):
    _logger.info(msg)


def error(msg):
    _logger.error(msg)


def warn(msg):
    _logger.warn(msg)


def set_level(level):
    _logger.set_level(level)


def set_color_log_mode():
    global _logger
    _logger = ColorLogger

def set_normal_log_mode():
    global _logger
    _logger = NormalLogger

