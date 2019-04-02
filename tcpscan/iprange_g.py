#!/usr/bin/pytheon3

import sys,os,time,argparse,socket

def check_ip(ip):
	a=[]
	rs=[]
	if len(ip.split(r'.'))==4:
		a=ip.split(r'.')
		for i in a:
			if int(i) < 0 or int(i) > 255:
				print("the ip range value include 0-255 int")
				sys.exit(0)
			else:
				rs.append(int(i))
	else:
		print("the ip range must be ipv4")
		sys.exit(0)
	return rs

def check_host(host):
	rs=[]
	if host != None:
		if type(host) == str:
			ns=socket.getaddrinfo(host,80)
			host_ip=ns[0][4][0]
			check_ip(host_ip)
			rs.append(host_ip)
		else:
			for i in host:
				ns=socket.getaddrinfo(i,80)
				host_ip=ns[0][4][0]
				check_ip(host_ip)
				rs.append(host_ip)
		return rs
	else:
		return 0

#check ip range input
def check_iprange(r):
	rs=[]
	if r != None:
		try:
			sr=r.split(r'-')
		except:
			print("The ip range input type must be int(0-255) and join with '-'")
			sys.exit(0)
		if len(sr)==2:
			print(sr)
			for i in sr:
				rs.extend(check_ip(i))
		else:
			print("The ip range input join with '-' and just only once")
			sys.exit(0)
		return rs

	else:
		return 0

#set start ip of the range
def set_seed(ipls):
	#split ip
	ipa=ipls[:4]
	ipb=ipls[4:]
	#set weight
	w=[8,4,2,1]
	w_ipa=0
	w_ipb=0
	x=[]
	for i in range(4):
		if ipa[i] < ipb[i]:
			w_ipb,w_ipa=w_ipb+w[i],w_ipa
			x.append(ipb[i]-ipa[i])
			break
		elif ipa[i] > ipb[i]:
			w_ipa,w_ipb=w_ipa+w[i],w_ipb
			x.append(ipa[i]-ipb[i])
			break
		elif ipa[i] == ipb[i]:
			w_ipa,w_ipb=w_ipa+w[i],w_ipb+w[i]
			x.append(0)
	z=len(x)
	#print('[set_seed]z = %s,w_ipa=%s,w_ipb=%s'%(z,w_ipa,w_ipb))
	if w_ipa > w_ipb:
		for i in range(4-z):
			e=ipa[i+z]-ipb[i+z]
			#print('[set_seed]e =',e)
			if e > 0:
				w_ipa,w_ipb=w_ipa+w[i+z],w_ipb
				x.append(e)
			elif e < 0:
				w_ipb,w_ipa=w_ipb+w[i+z],w_ipa
				x.append(e)
			elif e == 0:
				w_ipa,w_ipb=w_ipa+w[i+z],w_ipb+w[i+z]
				x.append(0)
	elif w_ipa < w_ipb:
		for i in range(4-z):
			e=ipb[i+z]-ipa[i+z]
			#print('[set_seed]z = %s,w_ipa=%s,w_ipb=%s'%(z,w_ipa,w_ipb))
			if e > 0:
				w_ipb,w_ipa=w_ipb+w[i+z],w_ipa
				x.append(e)
			elif e < 0:
				w_ipa,w_ipb=w_ipa+w[i+z],w_ipb
				x.append(e)
			elif e == 0:
				w_ipb,w_ipa=w_ipb+w[i+z],w_ipa+w[i+z]
				x.append(0)
	
	if w_ipa > w_ipb:
		return ipb,x
	elif w_ipa <= w_ipb:
		return ipa,x

def set_end(seed,count):
	r=''
	rlist=[]
	a,b,c,d=seed[0],seed[1],seed[2],seed[3]
	count+=d
	if count >= 256:
		d=count%256
		c+=int((count-d)/256)
		if c >= 256:
			x=c%256
			b+=int((c-x)/256)
			c=x
			if b >= 256:
				x=b%256
				a+=int((b-x)/256)
				b=x
	else:
		d=count
	'''for i in a,b,c,d:
		r+=str(i)+'.'
	r=r.rstrip('.')
	print('[set_end]ip end:',r)'''
	for i in a,b,c,d:
		rlist.append(i)
	return rlist

#ip generate
def ip_iter(seed,count):
	#print(seed,count)
	a,b,c,d=seed[0],seed[1],seed[2],seed[3]-1
	print("ip seed:",a,b,c,d)
	print("iter count:",count)	
	r=""
	while count > 0:
		r=""
		count-=1
		if d <= 255:
			d+=1
			if d > 255:
				d=0
				if c <= 255:
					c+=1
					if c > 255:
						c=0
						if b <= 255:
							b+=1
							if b > 255:
								b=0
								if a <= 255:
									a+=1
								else:
									print("out of ip range")
									break
								continue
						continue
				continue
		for i in a,b,c,d:
			r+=str(i)+'.'
			#print(r)
		r=r.rstrip('.')
		#print(r,"count:",count)
		yield r

def ip_host(host):
	if type(host) == str:
		yield host
		return
	else:
		for i in host:
			yield i

#the counts that how many ips need to scan
def ip_counts(ips):
	counts=0        
	for i in range(4):
		counts+=ips[1][i]*256**(3-i)
	return counts+1

if __name__=='__main__':
	parser=argparse.ArgumentParser(description='set host or ip range what will be scaned.')
	parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
	parser.add_argument('-host',type=str,nargs='*',default='127.0.0.1',help="set host list like '192.168.0.1 192.168.0.2' default 127.0.0.1")
	parser.add_argument('-range',type=str,help="set ip range to scan like '192.168.0.1-192.168.1.1' just once")
	parser.parse_args()
	args=parser.parse_args()

	host=args.host
	ipr=args.range

	#ipr="192.168.0.0-192.168.2.0"
	ip=check_iprange(ipr)
	host=check_host(host)
	if ip:
		print("ip range :",ip)
		ips=set_seed(ip)
		print('ips =',ips,type(ips))
		counts=ip_counts(ips)
		print("the ip range start ",ips[0]," counts ",counts)
		ipend=set_end(ips[0],counts)
		ipg=ip_iter(ips[0],counts)
		print('ipend :',ipend)
		for i in ipg:
			print(i)
	elif host:
		print('host :',type(host))
		print("host ip inclue:")
		g=ip_host(host)
		for i in g:
			print('host:',i)
	else:
		sys.exit(0)
