#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import pika

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)

import rabbitmq_settings

class RabbitMQ(object):
    def __init__(self, host=rabbitmq_settings.HOST, port=rabbitmq_settings.PORT, queue="vin"):
        self.host = host
        self.port = port
        self.queue = queue
        self.credentials = pika.PlainCredentials('admin', 'admin')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.host, self.port, '/', self.credentials))

    def publish(self, content):
        channel = self.connection.channel()
        channel.queue_declare(queue=self.queue)
        channel.basic_publish(exchange='', routing_key=self.queue, body=content)
        channel.close()

    def start_consuming(self, callback):
        channel = self.connection.channel()
        channel.queue_declare(queue=self.queue)
        channel.basic_consume(callback, queue=self.queue, no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def basic_get(self):
        channel = self.connection.channel()
        result = None
        msg = channel.basic_get(queue=self.queue)
        if msg[0] is not None:
            channel.basic_ack(msg[0].delivery_tag)
            return msg[2]
        channel.close()
        return result


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


def main():
    import time
    mq = RabbitMQ(queue="test")
    for i in range(5):
        mq.publish("hello, world, @%f" % (time.time()))
    print "basic get:", mq.basic_get()
    mq.start_consuming(callback)


if __name__ == '__main__':
    main()
