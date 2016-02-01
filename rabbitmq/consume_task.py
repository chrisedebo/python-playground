<<<<<<< HEAD
#! /usr/bin/env python2.7
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
  'localhost'))

channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch,method,properties,body):
    print(" [x] Received %r" % (body,))
    time.sleep( body.count('.') )
    print(" [x] Done")

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()

connection.close
=======
#! /usr/bin/env python2.7
import pika
import time
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(
  'localhost'))

channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch,method,properties,body):
    print(" [x] Received %r" % (body,))
    decoded = json.loads((body,))
    print 'DECODED:', decoded
    print(" [x] Done")

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()

connection.close
>>>>>>> 5373d7b508e85fad821eb6919378d6f8ef2ce868
