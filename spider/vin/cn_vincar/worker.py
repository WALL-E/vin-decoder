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
from robot import robot_html
from parse import parse_html


def do_task(vin_code):
    """
    Execute query VIN task

    :vin_code: The 17 character VIN
    :returns: list or None
    """
    print "do_task(): %s" % (vin_code)
    html = robot_html(vin_code)
    if html is not None:
        results = parse_html(html)  
        return results
    else:
        print "%s not found, download page failed" % (vin_code)
    return None


def do_once(vin_code):
    results = do_task(vin_code)
    if results:
        Mongo().insert_vin(results, vin_code)
    print "result: %s" % (results)


def do_loop():
    mq = RabbitMQ(queue="vin")
    while True:
        vin_code = mq.basic_get()
        if vin_code:
            print "vinCode: %s" % (vin_code)
            results = do_task(vin_code)
            if results:
                Mongo().insert_vin(results, vin_code)
            else:
                # Requeue
                mq.publish(vin_code)
            print "result: %s" % (results)
        else:
            print "no topic, to sleep 10 sec ..."
            time.sleep(10)
        time.sleep(5)


def main():
    if len(sys.argv) == 2:
        vin_code = sys.argv[1]
        do_once(vin_code)
    else:
        do_loop()
    
if __name__ == '__main__':
    main()
