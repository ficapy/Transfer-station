#!/usr/bin/env python
#-*- coding: utf-8 -*-

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks,returnValue
from autobahn.twisted.util import sleep
from info import getinfo
from download import download
from downloadstatus import getstatus, getCurrentTask
from autobahn import wamp
from uuid import uuid4
from random import randint
from utils import initcheck,noblockprocess,rm

SAVEPATH = r"/home/download"
WEBFSDPORT = "7788"
initcheck.webfsd(SAVEPATH, WEBFSDPORT)

class GetInfoComponent(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self)
        while True:
            # df -h every minutes
            if randint(1,200)>199:
                df = yield noblockprocess.noblock("df","-h")
                self.publish("getdf", (df.split()[8],df.split()[11]))
            if randint(1,200)>199:
                free = yield noblockprocess.noblock("free","-m")
                self.publish("getfree", (free.split()[7], free.split()[8]))
            result = yield getCurrentTask()
            yield sleep(0.3)
            for i in result:
                uuid, downloadinfo = i[0], i[1:]
                self.publish(uuid, downloadinfo)


    # URI都来个正则匹配无法大写也是够蛋疼的
    @wamp.register(u"getdownloadstatus")
    def statusComponent(self, uuid):
        return getstatus(uuid)

    @wamp.register(u"getfileinfo")
    def getinfoComponent(self, url):
        return getinfo(url)

    @wamp.register(u"calldownload")
    def startDownload(self, url, ext, height=""):
        uuid = str(uuid4()).replace("-","")
        rm.rm(SAVEPATH)
        return download(uuid, url, ext, height,SAVEPATH)


    @wamp.register(u"getdf")
    def getdf(self):
        def process(df):
            return df.split()[8],df.split()[11]
        return noblockprocess.noblock("df","-h").addCallback(process)

    @wamp.register(u"getfree")
    def getfree(self):
        def process(free):
            return free.split()[7], free.split()[8]
        return noblockprocess.noblock("free","-m").addCallback(process)


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1")
    runner.run(GetInfoComponent)