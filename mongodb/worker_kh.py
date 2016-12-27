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

from rabbitmq import RabbitMQ

base_url = "http://spider.xxx.com/CarInfo/vinQuery"
timeout = 60

client = MongoClient()
client = MongoClient("localhost", 27017)
db = client["vin"]
collection = db["vin"]


def do_task(vin_code):
    print "do_task(): %s" %(vin_code)
    payload = {"vinCode": vin_code}
    response = requests.post(base_url, timeout=timeout, data=payload)

    if response.status_code == 200:
        data = json.loads(response.text)
        print data
        if data["status"] == "20000000":
            result = data["result"]
            result["vinCode"] = result["vinCode"][0:8]
            collection.insert(result)
        else:
            print "[1] %s not found" % (vin_code)
    else:
        print "[2] %s not found" % (vin_code)


def main():
    if len(sys.argv) == 2:
        vin_code = sys.argv[1]
        do_task(vin_code)
        sys.exit(1)
    
    while True:
        mq = RabbitMQ(queue="vin")
        msg = mq.basic_get()
        if msg:
            print msg
            vin_code = msg
            do_task(vin_code)
        else:
            print "no topic, to sleep 10 sec ..."
            time.sleep(10)
        time.sleep(30)

if __name__ == '__main__':
    main()
