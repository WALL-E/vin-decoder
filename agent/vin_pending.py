#!/usr/bin/python

import sys
import os

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../rabbitmq'))

from rabbitmq import RabbitMQ

def next_vin_code():
    mq = RabbitMQ(queue="vin")
    return mq.basic_get()

if __name__ == '__main__':
    vin_code = next_vin_code()
    if vin_code:
        print vin_code
    else:
        print "no vin-pengding"
