#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rabbitmq import RabbitMQ
import time
import sys

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

def main():
    queue = "vin"
    if len(sys.argv) >= 2:
        queue = sys.argv[1]
    mq = RabbitMQ(queue=queue)
    mq.start_consuming(callback)

if __name__ == '__main__':
    main()
