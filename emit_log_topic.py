#!/usr/bin/env python
#-*- coding: utf-8 -*-

# function: xxx
# author: jmhuang@corp.netease.com
# create_time: 2018/7/17

import sys
import pika

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs',
                             exchange_type="topic")
    routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
    message = ''.join(sys.argv[2:]) or "Hello World!"
    channel.basic_publish(exchange="topic_logs",
                          routing_key=routing_key,
                          body=message)
    print "[x] Sent %r:%r" % (routing_key, message)
    connection.close()