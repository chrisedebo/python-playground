#!/usr/bin/env python

import socket

UDP_IP = "10.0.3.188"
UDP_PORT = 14000
MESSAGE = "/jmn;127.0.0.1;1234"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
