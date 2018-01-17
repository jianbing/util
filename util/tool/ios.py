#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created by jianbing on 2017-11-06
"""
import os
import plistlib
import traceback


def get_bundle_identifier(file_path):
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file == 'Info.plist':
                with open(os.path.join(root, file), 'rb') as plist_file:
                    plist = plistlib.loads(plist_file.read())
                    try:
                        return plist['CFBundleIdentifier'], plist['CFBundleShortVersionString'], plist['CFBundleVersion']
                    except:
                        traceback.print_exc()
                        print(plist)
                        return
    raise Exception("can not find Info.plist")