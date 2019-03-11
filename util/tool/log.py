#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import inspect
import logging
import logging.handlers
from colorama import Fore, Style


class _ColorLogger:
    def __init__(self):
        self._logger = logging.getLogger('color_logger')
        self._logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        self._logger.addHandler(handler)

    def debug(self, msg):
        self._logger.debug("DEBUG " + str(msg) +
                           "    Func:{} Line:{} File:{}".format(*self._get_inspect_info()) +
                           Style.RESET_ALL)

    def info(self, msg):
        self._logger.info(Fore.GREEN + "INFO " + str(msg) +
                          "    Func:{} Line:{} File:{}".format(*self._get_inspect_info()) +
                          Style.RESET_ALL)

    def warn(self, msg):
        self._logger.warning(Fore.YELLOW + "WARNING " + str(msg) +
                             "    Func:{} Line:{} File:{}".format(*self._get_inspect_info()) +
                             Style.RESET_ALL)

    def error(self, msg):
        self._logger.error(Fore.RED + "ERROR " + str(msg) +
                           "    Func:{} Line:{} File:{}".format(*self._get_inspect_info()) +
                           Style.RESET_ALL)

    def set_level(self, level):
        self._logger.setLevel(level)

    def _get_inspect_info(self):
        stack = inspect.stack()
        return stack[3].function, stack[3].lineno, os.path.basename(stack[3].filename)


_logger = _ColorLogger()


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


def set_level_to_debug():
    _logger.set_level(logging.DEBUG)


def set_level_to_info():
    _logger.set_level(logging.INFO)


def set_level_to_warn():
    _logger.set_level(logging.WARN)


def set_level_to_error():
    _logger.set_level(logging.ERROR)
