#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from util.tool import log

if __name__ == '__main__':
    log.set_level_to_info()
    log.debug("debug msg")
    log.info("info msg")
    log.warn("warn msg")
    log.error("error msg")
