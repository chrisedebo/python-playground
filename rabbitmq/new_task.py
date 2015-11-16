#! /usr/bin/env python2.7
import pika
import sys
import json

message = ' '.join(sys.argv[1:]) or "Hello World!"

def broadcast (message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
      'localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)
    print(" [x] Sent '",message,"'")
    connection.close

data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
broadcast(repr(data))

data_string = json.dumps(data)
broadcast(data_string)

json_string = '''{ "firstName": "John","age": 25,"address": {"streetAddress": "21 2nd Street","city": "New York","state": "NY","postalCode": "10021"},"phoneNumber": [{"type": "home","number": "212 555-1234"},{"type": "fax","number": "646 555-4567"}]}'''

broadcast(json_string)
