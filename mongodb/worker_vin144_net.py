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
            return result
        else:
            print "[1] %s not found, parse html failed" % (vin_code)
    else:
        print "[2] %s not found, download page failed" % (vin_code)
    return None


def peek_task(vin_code):
    data = do_task(vin_code)
    print "result: %s" % (data)

def loop_task():
    mq = RabbitMQ(queue="vin")
    while True:
        vin_code = mq.basic_get()
        if vin_code:
            print "vinCode: %s" % (vin_code)
            data = do_task(vin_code)
            if data is None:
                # Requeue
                mq.publish(vin_code)
            else:
                collection.insert(data)
            print "result: %s" % (data)
        else:
            print "no topic, to sleep 10 sec ..."
            time.sleep(10)
        time.sleep(5)

def main():
    if len(sys.argv) == 2:
        vin_code = sys.argv[1]
        peek_task(vin_code)
    else:
        loop_task()
    
if __name__ == '__main__':
    main()
