#!/usr/bin/env python
#-*- coding: utf-8 -*-

# function: xxx
# author: jmhuang@corp.netease.com
# create_time: 2018/7/17

import pika
import time


def callback(ch, method, properties, body):
    print " [x] Received %r" % body
    time.sleep(body.count('.'))
    print " [x] Done"
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue="task_queue", durable=True)
    print ' [*] Waiting for messages. To exit press CTRL+C'

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                          queue='task_queue')
    channel.start_consuming()
