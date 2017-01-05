#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time
import sys
import os
import requests

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '..'))

from rabbitmq.rabbitmq import RabbitMQ

home_url = "http://ip.cn/"
timeout = 10

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    proxies = {
        "http": "http://%s"%(body)
    }
    try:
        response = requests.get(home_url, proxies=proxies, timeout=timeout)
        mq = RabbitMQ(queue="proxy")
        mq.publish(body)
        print "%s is good" % (body)
    except requests.exceptions.ConnectTimeout:
        pass
    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectionError:
        pass


def main():
    queue = "kuaidaili"
    if len(sys.argv) >= 2:
        queue = sys.argv[1]
    mq = RabbitMQ(queue=queue)
    mq.start_consuming(callback)

if __name__ == '__main__':
    main()

