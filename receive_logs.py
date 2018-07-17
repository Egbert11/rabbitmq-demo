#!/usr/bin/env python
#-*- coding: utf-8 -*-

# function: xxx
# author: jmhuang@corp.netease.com
# create_time: 2018/7/17

import pika
import time


def callback(ch, method, properties, body):
    print " [x] %r" % body


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange="logs",
                             exchange_type="fanout")
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs',
                       queue=queue_name)
    print ' [*] Waiting for logs. To exit press CTRL+C'

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
    channel.start_consuming()
