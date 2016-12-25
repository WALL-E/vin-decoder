#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
worker: query vin
"""

import sys
import json
import os
import time

import requests

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../../../rabbitmq'))
sys.path.append(os.path.join(ROOT_DIR, '../../../mongodb'))

from rabbitmq import RabbitMQ
from mongo import Mongo

URL = "http://spider.51kahui.com/CarInfo/vinQuery"
TIMEOUT = 60


def do_task(vin_code):
    """
    Execute query VIN task

    :vin_code: The 17 character VIN
    :returns: list or None
    """
    print "do_task(): %s" %(vin_code)
    payload = {"vinCode": vin_code}
    response = None
    data = None
    try:
        response = requests.post(URL, timeout=TIMEOUT, data=payload)
    except Exception, msg:
        print "Exception: ", msg

    if response is not None and response.status_code == 200:
        data = json.loads(response.text)
        # print data
        if data["status"] == "20000000":
            result = data["result"]
            data = [result]
        else:
            print "[1] %s not found, access restricted" % (vin_code)
    else:
        print "[2] %s not found, network fault" % (vin_code)
    return data


def do_once(vin_code):
    results = do_task(vin_code)
    if results:
        Mongo().insert_vin(results, vin_code)
    print results


def do_loop():
    mq = RabbitMQ(queue="vin")
    db = Mongo()
    while True:
        msg = mq.basic_get()
        if msg:
            vin_code = msg
            results = do_task(vin_code)
            if results:
                db.insert_vin(results, vin_code)
            else:
                mq.publish(vin_code)
            print "final result: %s" % (results)
        else:
            print "no topic, to sleep 10 sec ..."
            time.sleep(10)
        #time.sleep(300)


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
