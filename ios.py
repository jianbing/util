#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from utils.tools.biplist import *


def get_bundle_identifier(path):
    for root, dirs, files in os.walk(path):
        for afile in files:
            if afile == 'Info.plist':
                plist = readPlist(os.path.join(root,afile))
                return plist['CFBundleIdentifier'], plist['CFBundleShortVersionString'], plist['CFBundleVersion']

    raise Exception("can not find Info.plist")