#!/usr/bin/env python
#-*- coding: utf-8 -*-

# function: xxx
# author: jmhuang@corp.netease.com
# create_time: 2018/7/17

import sys
import pika
import time


def callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body)


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange="topic_logs",
                             exchange_type="topic")
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys:
        channel.queue_bind(exchange='topic_logs',
                           queue=queue_name,
                           routing_key=binding_key)

    print ' [*] Waiting for logs. To exit press CTRL+C'

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
    channel.start_consuming()
