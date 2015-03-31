#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import time
import subprocess
import os
import fcntl

try:
    import youtube_dl
except ImportError:
    print("before run this script please use 'sudo pip install youtube-dl'")
    sys.exit()

from os import path

if not path.exists('/usr/local/bin/youtube-dl'):
    print("be sure youtube-dl paths is correct")
    sys.exit()
if not path.exists('/usr/local/bin/youtube-dl'):
    print("be sure youtube-dl paths is correct")
    sys.exit()
try:
    a = subprocess.Popen(["webfsd"], stderr=subprocess.PIPE)
    a.kill()
except OSError as e:
    print e
    print "before use 'sudo apt-get install webfs' install webfsd"
    sys.exit()


# https://gist.github.com/sebclaeys/1232088
def _non_block_read(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except Exception as er:
        return er

def webfsd(filedir, port):
    assert all(map(lambda x: isinstance(x, str), [filedir, port]))
    if not path.exists(filedir):
        print("webfsd save file paths not exists")
        sys.exit()
    b = subprocess.Popen(["sudo","killall", "webfsd"])
    b.wait()
    a = subprocess.Popen(["webfsd", "-r", filedir, "-p", port], stderr=subprocess.PIPE)
    time.sleep(1)
    if bool(_non_block_read(a.stderr)):
        print _non_block_read(a.stderr)
        print "use sudo killall webfsd"
        sys.exit()
