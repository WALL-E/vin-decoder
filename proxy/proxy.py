#!/usr/bin/env python2.7

import sys
import os

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '..'))

from rabbitmq.rabbitmq import RabbitMQ

def next_server():
    mq = RabbitMQ(queue="proxy")
    return mq.basic_get()

def requeue_server(server):
    mq = RabbitMQ(queue="proxy")
    mq.publish(server)

if __name__ == '__main__':
    proxy = next_server()
    if proxy:
        print proxy
    else:
        print "no proxy"
