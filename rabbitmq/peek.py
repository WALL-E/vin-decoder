#!/usr/bin/python

import sys
import os

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../rabbitmq'))

from rabbitmq import RabbitMQ

def peek(queue):
    mq = RabbitMQ(queue=queue)
    msg = mq.basic_get()
    mq.publish(msg)
    return msg

if __name__ == '__main__':
    queue = "vin"
    if len(sys.argv) == 2:
        queue = sys.argv[1]
    msg = peek(queue)
    if msg:
        print msg
    else:
        print "no msg @%s" %(queue)
