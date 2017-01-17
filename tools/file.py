#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import time
import shutil


class File(object):

    def __init__(self, file_path):
        self._file_path = file_path

    @property
    def path(self):
        return self._file_path

    @property
    def is_dir(self):
        return os.path.isdir(self._file_path)

    @property
    def suffix(self):
        if self.is_dir:
            return None
        return self._file_path.split(".")[-1]

    @property
    def exists(self):
        return os.path.exists(self._file_path)

    @property
    def basename(self):
        return os.path.basename(self._file_path)

    @property
    def modify_time(self):
        return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(os.stat(self._file_path).st_mtime))

    @property
    def size(self):
        return os.path.getsize(self._file_path)

    def move(self, dst):
        shutil.move(self._file_path, dst)
