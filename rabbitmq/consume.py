#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rabbitmq import RabbitMQ
import time

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

def main():
    mq = RabbitMQ()
    mq.start_consuming(callback)

if __name__ == '__main__':
    main()
