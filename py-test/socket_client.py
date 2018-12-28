#!/usr/bin/python3

import socket
import sys
import time
import os

print("start time:",time.ctime()) 

# create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# get host and port
host='192.168.254.1'
port=135

addrinfo=socket.getaddrinfo(host,port)

print(host,port,"\n")

print(addrinfo[0][4])

# to server and return port status
constat=s.connect_ex((host,port))
time.sleep(1)
c=os.strerror(constat)
print ("host:",host,"port:",port,"=>",c)

#send data
#msgsend = b"123123123123123"
#s.send(msgsend)

#close socket object
s.close()

print("end time:",time.ctime())

