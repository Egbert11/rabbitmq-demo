#!/usr/bin/env python
#-*- coding: utf-8 -*-

# function: xxx
# author: jmhuang@corp.netease.com
# create_time: 2018/7/17

import sys
import pika
from pprint import pprint

def fib(n):
    if n in (0, 1):
        return n
    else:
        return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body):
    n = int(body)
    print " [.] fib(%s)" % n
    print "ch:%s,method:%s,props:%s,body:%s" % (ch, method, props, body)
    print "ch:%s,method:%s,props:%s" % (vars(ch), vars(method), vars(props))
    print "ch:%s,method:%s,props:%s" % (pprint(vars(ch)), pprint(vars(method)), pprint(vars(props)))

    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue="rpc_queue")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue="rpc_queue")

    print "[x] Awaiting RPC requests"
    channel.start_consuming()