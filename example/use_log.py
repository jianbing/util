#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from util import log
from util.log.loglevel import LogLevel

if __name__ == '__main__':

    log.set_level(LogLevel.INFO)
    log.debug("debug msg")
    log.error("error msg")
    log.info("info msg")
    log.warn("warn msg")
