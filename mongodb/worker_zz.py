#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import sys
import json
import os
import time

from pymongo import *

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../rabbitmq'))
sys.path.append(os.path.join(ROOT_DIR, '../agent'))
sys.path.append(os.path.join(ROOT_DIR, '../html'))

from rabbitmq import RabbitMQ
from robot import robot_html_vin144_net
from parse import parse_html_vin114_net

timeout = 60

client = MongoClient()
client = MongoClient("localhost", 27017)
db = client["vin"]
collection = db["vin"]


def do_task(vin_code):
    print "do_task(): %s" % (vin_code)
    html = robot_html_vin144_net(vin_code)
    if html is not None:
        result = parse_html_vin114_net(html)  
        if result is not None:
            result["vinCode"] = vin_code[0:8]
            collection.insert(result)
            return result
        else:
            print "[1] %s not found, parse html failed" % (vin_code)
    else:
        print "[2] %s not found, download page failed" % (vin_code)
    return None


def main():
    if len(sys.argv) == 2:
        vin_code = sys.argv[1]
        data = do_task(vin_code)
        # print "result: %s" % (data)
        print "result: %s" % (json.dumps(data, ensure_ascii=False))
        sys.exit(1)
    
    mq = RabbitMQ(queue="vin")
    while True:
        msg = mq.basic_get()
        if msg:
            print "vinCode: %s" % (msg)
            vin_code = msg
            data = do_task(vin_code)
            print "result: %s" % (data)
        else:
            print "no topic, to sleep 10 sec ..."
            time.sleep(10)
        time.sleep(5)

if __name__ == '__main__':
    main()
