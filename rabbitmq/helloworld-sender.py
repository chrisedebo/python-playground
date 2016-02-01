<<<<<<< HEAD
#! /usr/bin/env python2.7
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
  'localhost'))

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")

connection.close
=======
#! /usr/bin/env python3.3
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
  'localhost'))

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")

connection.close
>>>>>>> 5373d7b508e85fad821eb6919378d6f8ef2ce868
