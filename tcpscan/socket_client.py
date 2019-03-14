#!/usr/bin/python3.5

import socket,time,os,sys

if __name__=='__main__':
	st=time.time()

	# create socket object
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	# get host and port
	host='127.0.0.1'
	port=22
	addrinfo=socket.getaddrinfo(host,port)
	print(addrinfo[0][4])

	# to server and return port status
	constat=s.connect_ex((host,port))
	c=os.strerror(constat)
	print ("host:",host,"port:",port,"->",c)
	s.close()

	print("use time :%.4f"%(time.time()-st))

