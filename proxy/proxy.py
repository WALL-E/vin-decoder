#!/usr/bin/python

import sys
import os

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../rabbitmq'))

from rabbitmq import RabbitMQ

def next_server():
    mq = RabbitMQ(queue="proxy")
    return mq.basic_get()

if __name__ == '__main__':
    proxy = next_server()
    if proxy:
        print proxy
    else:
        print "no proxy"
