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

    channel.exchange_declare(exchange='logs',
                             exchange_type="fanout")
    message = ''.join(sys.argv[1:]) or "info: Hello World!"
    channel.basic_publish(exchange="logs",
                          routing_key='',
                          body=message)
    print "[x] Sent %r" % message
    connection.close()