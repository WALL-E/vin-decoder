#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from rabbitmq import RabbitMQ
import time
import sys

def main():
    queue = "vin"
    if len(sys.argv) >= 2:
        queue = sys.argv[1]
    mq = RabbitMQ(queue=queue)
    msg = mq.basic_get()
    if msg:
        print msg
    else:
        print "no topic"

if __name__ == '__main__':
    main()
