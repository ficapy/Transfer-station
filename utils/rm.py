#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, remove, listdir
from time import time

def rm(Path):
    for i in listdir(Path):
        if time() - path.getmtime(path.join(Path, i)) > 30 * 60:
            remove(path.join(Path, i))

