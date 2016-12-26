#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

class RabbitMQ():
    def __init__(self, host="localhost", port=5672, queue="vin"):
        self.host = host
        self.port = port
        self.queue = queue

    def publish(self, content):
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.host, self.port, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue)
        channel.basic_publish(exchange='', routing_key=self.queue, body=content)
        connection.close()

    def start_consuming(self, callback):
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.host, self.port, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue)
        channel.basic_consume(callback, queue=self.queue, no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def basic_get(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.host, self.port, '/', credentials))
        channel = connection.channel()
        msg = channel.basic_get(queue=self.queue)
        if msg[0] is not None:
            channel.basic_ack(msg[0].delivery_tag)
            return msg[2]
        return None


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


if __name__ == '__main__':
    import time
    mq = RabbitMQ(queue="test")
    for i in range(5):
        mq.publish("hello, world, @%f" % (time.time()))
    mq.start_consuming(callback)
