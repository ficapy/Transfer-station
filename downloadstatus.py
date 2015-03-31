#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from os import path
import datetime
from twisted.enterprise import adbapi

dbpath = "/vagrant/youtube.db"

if not path.exists(dbpath):
    db = sqlite3.connect(dbpath)
    cur = db.cursor()
    cur.execute("""
                     CREATE TABLE youtube (
                        uuid              TEXT     NOT NULL,
                        rate             NUMBER   NOT NULL,
                        total            TEXT   NOT NULL ,
                        speed           TEXT    NOT NULL,
                         eta             TEXT   NOT NULL,
                         url             TEXT   NOT NULL ,
                         create_time   TEXT   NOT NULL ,
                         cost_time      TEXT  NOT NULL ,
                        PRIMARY KEY (uuid))
                     """)

    db.commit()
    db.close()

dbpool = adbapi.ConnectionPool("sqlite3", dbpath, check_same_thread=False)


def _insert(txn, uuid, rate, total, speed, eta, url, cost_time="0"):
    if cost_time == "0":
        txn.execute("SELECT * FROM youtube WHERE uuid= ?", (uuid, ))
        result = txn.fetchall()
        if not result:
            txn.execute("INSERT INTO youtube VALUES (?,?,?,?,?,?,?,?)",
                        (uuid, rate, total, speed, eta, url, datetime.datetime.now(), cost_time))
        else:
            txn.execute("UPDATE youtube SET rate=?,total=?,speed=?,eta=?,create_time=?, cost_time=? WHERE uuid=?",
                        (rate, total, speed, eta, datetime.datetime.now(), cost_time, uuid))
    else:
        txn.execute("UPDATE youtube SET cost_time=? WHERE uuid=?", (cost_time, uuid))


def insert(uuid, rate, total, speed, eta, url, cost_time="0"):
    # return dbpool.runQuery("SELECT * FROM youtube WHERE uuid= ?", (uuid,))
    dbpool.runInteraction(_insert, uuid, rate, total, speed, eta, url, cost_time)


def _getstatus(txn, uuid):
    txn.execute("SELECT * FROM youtube WHERE uuid= ?", (uuid,))
    result = txn.fetchall()
    return result[-1]


def getstatus(uuid):
    return dbpool.runInteraction(_getstatus, uuid)


def getCurrentTask():
    return dbpool.runQuery("""SELECT * FROM youtube WHERE \
    (strftime('%s','now')-strftime('%s', create_time))<100000""")



