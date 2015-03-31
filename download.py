#!/usr/bin/env python
#-*- coding: utf-8 -*-

from twisted.internet.protocol import ProcessProtocol
from twisted.internet.defer import Deferred
from twisted.internet import reactor
from downloadstatus import insert


class WgetProcess(ProcessProtocol):
    def __init__(self, deferred, uuid, url):
        self.uuid = uuid
        self.url = url
        self.deferred = deferred
        self.flag = True

    def outReceived(self, data):
        print data
        if len(data.split()) == 8 and "[download]" in data and "ETA" in data and "of" in data:
            # 没找到好的办法利用autobahn实时发布，能下载直接返回成功
            if self.flag:
                self.deferred.callback(self.uuid)
                self.flag = False
            result = float(data.split()[1][:-1]),data.split()[3], \
                     data.split()[5], data.split()[7], self.url
            insert(self.uuid, *result)

        # [download] 100% of 4.24MiB  ----------→exists
        elif len(data.split()) == 4 and "[download] 100% of" in data and "MiB" in data:
            insert(self.uuid, rate=100, total=data.split()[-1], speed=1000.0, eta="00:00", url=self.url)
            # print "already exists"
            self.deferred.callback(self.uuid)
            
        # [download] 100% of 135.08KiB in 00:01 ------→download done
        elif len(data.split()) == 6 and "[download] 100% of" in data and "KiB in" in data:
            cost_time = data.split()[-1]
            arg = list(xrange(5))
            arg.append(cost_time)
            insert(self.uuid, *arg)
            # print u"本机已存在"
            # self.deferred.callback("True")


def download(uuid, url, ext, height,savepath):
    deferred = Deferred()
    deferred.addCallback(lambda x: x)
    if height:
        options = "[ext={}][height={}]".format(ext, height)
    else:
        options = "/audio/{}".format(ext) #下载音频
    reactor.spawnProcess(WgetProcess(deferred, uuid, url), '/usr/local/bin/youtube-dl',
                         ["youtube-dl", "-f", options, "-o","{}/%(title)s".format(savepath),url], usePTY=True)
    return deferred