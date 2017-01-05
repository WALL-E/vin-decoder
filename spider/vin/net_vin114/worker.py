#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
"""
worker: query vin
"""

import sys
import json
import os
import time
import copy

import requests

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../../..'))
sys.path.append(os.path.join(ROOT_DIR, '../../..'))

from rabbitmq.rabbitmq import RabbitMQ
from mongodb.mongodb import MongoDB
from robot import robot_html
from parse import parse_html

import settings


def do_attach(objs, vin_code, origin):
    """
    additional data: vinCode,vinLong,origin
    """
    now = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
    for obj in objs:
        obj["vinCode"] = vin_code[0:8]
        obj["vinLong"] = vin_code
        obj["origin"] = origin
        obj["timestamp"] = now
    return objs


def do_task(vin_code):
    """
    Execute query VIN task

    :vin_code: The 17 character VIN
    :returns: list or None
    """
    print "do_task(): %s" % (vin_code)
    html = robot_html(vin_code, proxy_use=settings.PROXY_USE, proxy_reuse=settings.PROXY_REUSE)
    if html is not None:
        results = parse_html(html)  
        if results:
            return do_attach(results, vin_code, settings.ORIGIN)
        else:
            print "[1] %s not found, parse html failed" % (vin_code)
    else:
        print "[2] %s not found, download page failed" % (vin_code)
    return None


def do_once(vin_code):
    results = do_task(vin_code)
    if results:
        MongoDB().insert_vin(results)
    print "result: %s" % (results)


def do_loop():
    mq = RabbitMQ(queue="vin")
    db = MongoDB()
    while True:
        vin_code = mq.basic_get()
        if vin_code:
            print "vinCode: %s" % (vin_code)
            results = do_task(vin_code)
            if results:
                db.insert_vin(results)
            else:
                # Requeue
                mq.publish(vin_code)
            print "final result: %s" % (results)
        else:
            print "no topic, to sleep 10 sec ..."
            time.sleep(10)
        time.sleep(5)


def main():
    """
    main function
    """
    if len(sys.argv) == 2:
        vin_code = sys.argv[1]
        do_once(vin_code)
    else:
        do_loop()


if __name__ == '__main__':
    main()
