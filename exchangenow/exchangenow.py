#! /usr/bin/env python3.4
import json
import io
import sys
#Read http api
#Convert to json object
#Store in DB
#Do stuff
#Send Alert

import http.client
conn = http.client.HTTPSConnection("api.cryptonator.com")
try:
    conn.request("GET", "/api/full/btc-zec")
    r1 = conn.getresponse()
except:
    print("Unexpected error:", sys.exc_info()[0])
    exit(1)
    
if r1.status != 200:
    print(r1.status, r1.reason)
    exit(r1.status)

data1 = r1.read()  # This will return entire content.
#print(data1)
conn.close()

jsondata = json.loads(data1.decode("utf-8"))
print(jsondata)

print(jsondata["timestamp"])
print(jsondata["ticker"])

import mysql.connector as mariadb
dbhost="localhost"
db="exchangenow"
dbuser="exchangenow"
dbpass="JwhV6Fzh9ySLU5Lq"

mariadb.connect(user=dbuser,password=dbpass,database=db)

