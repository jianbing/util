#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from colorama import Fore, Back, Style
import sys
import logging.handlers
_logger = logging.getLogger('logger')
_logger.setLevel(logging.DEBUG)
_logger_handler = logging.StreamHandler(sys.stdout)
_logger_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
_logger.addHandler(_logger_handler)


def debug(msg):
    _logger.debug("DEBUG " + str(msg))


def info(msg):
    _logger.debug("INFO " + str(msg))


def error(msg):
    _logger.debug(Fore.RED + "ERROR " + str(msg) + Style.RESET_ALL)


def warning(msg):
    _logger.debug(Fore.YELLOW + "WARNING " + str(msg) + Style.RESET_ALL)


def set_level(level):
    _logger.setLevel(level)
