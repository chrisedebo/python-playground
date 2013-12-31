#! /usr/bin/env python2.7
import pika
import sys

message = ' '.join(sys.argv[1:]) or "Hello World!"

connection = pika.BlockingConnection(pika.ConnectionParameters(
  'localhost'))

channel = connection.channel()

channel.queue_declare(queue='hello')



channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

print(" [x] Sent 'Hello World!'")

connection.close
