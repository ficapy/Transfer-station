#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet.protocol import ProcessProtocol
from twisted.internet.defer import Deferred
from twisted.internet import reactor


class NoBlockProcess(ProcessProtocol):
    def __init__(self, deferred):
        self.data = ""
        self.deferred = deferred

    def outReceived(self, data):
        self.data += data

    def processEnded(self, reason):
        self.deferred.callback(self.data)


def noblock(process, optionals=""):
    deferred = Deferred()
    deferred.addCallback(lambda x: x)
    op = [process]
    op.extend(optionals.split())
    op = filter(bool,op) # 去掉空参数
    reactor.spawnProcess(NoBlockProcess(deferred), process, op, usePTY=True)
    return deferred

# df -h -------ubuntu14.10
# b.split()[8],b.split()[11]
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1        40G  1.5G   37G   4% /
# none            4.0K     0  4.0K   0% /sys/fs/cgroup
# udev            240M  4.0K  240M   1% /dev
# tmpfs            49M  940K   49M   2% /run
# none            5.0M     0  5.0M   0% /run/lock
# none            245M     0  245M   0% /run/shm
# none            100M     0  100M   0% /run/user
# vagrant          26G   12G   14G  46% /vagrant

# free -m
# b.split()[7], b.split()[8]
#              total       used       free     shared    buffers     cached
# Mem:           489        469         20          1          1         37
# -/+ buffers/cache:        430         59
# Swap:            0          0          0
