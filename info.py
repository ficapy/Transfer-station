# coding:utf-8

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet.defer import Deferred
import json



class InfoProcessProtocol(protocol.ProcessProtocol):
    data = ""

    def __init__(self, deferred):
        self.deferred = deferred

    def outReceived(self, data):
        self.data += data

    def processEnded(self, reason):
        try:
            info = json.loads(self.data)
            item = []
            for v in info.get("formats"):
                #剔除一些不需要的项目
                if v.get("format_note") and "x" not in v.get("format") and not v.get("filesize"):
                    item.append({"format": v.get("format").split(' - ')[-1].lstrip(),
                                 "ext": v.get("ext")})
            result = json.dumps({
                "url": info.get("webpage_url"),
                "title": info.get("title"),
                "items": item
            })
            self.deferred.callback(result)
        except:
            self.deferred.errback(Exception("error"))



def getinfo(url):
    # http://www.youtube.com/watch?v=-wNyEUrxzFU
    d = Deferred()
    d.addCallback(lambda x:x)
    reactor.spawnProcess(InfoProcessProtocol(d), '/usr/local/bin/youtube-dl', ["youtube-dl",
                                                                               "--socket-timeout", "5",
                                                                               "--skip-download",
                                                                               "--print-json", "--newline",
                                                                               url])
    return d


