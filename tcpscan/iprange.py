#!/usr/bin/pytheon3

import sys,os,time,argparse

parser=argparse.ArgumentParser(description='set host or ip range what will be scaned.')
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
parser.add_argument('-host',type=str,nargs='*',default='127.0.0.1',help="set host list like '192.168.0.1 192.168.0.2' default 127.0.0.1")
parser.add_argument('-range',type=str,help="set ip range to scan like '192.168.0.1-192.168.1.1' just once")
parser.parse_args()
args=parser.parse_args()

host=args.host
ipr=args.range

#ipr="192.168.0.0-192.168.2.0"

#check ip range input
def ip_check(r):
	a=[]
	rs=[]
	if r:
		try:
			if len(r.split(r'-'))==2:
				sr=r.split(r'-')
				for i in sr:
					if len(i.split(r'.'))==4:
						a=i.split(r'.')
						for i in a:
							if int(i) < 0 or int(i) > 255:
								print("the ip range value include 0-255 int")
								sys.exit(0)
							else:
								rs.append(int(i))
					else:
						print("the ip range must be ipv4")
						sys.exit(0)
			else:
				print("The ip range input join with '-' and just only once")
				sys.exit(0)
			return rs
		except:
			print("The ip range input type must be int(0-255) and join with '-'")
			sys.exit(0)
	else:
		return

#set start ip of the range
def set_seed(ipls):
	#split ip
	ipa=ipls[:4]
	ipb=ipls[4:]

	#set weight
	w=[8,4,2,1]
	w_ipa=0
	w_ipb=0

	g=[]
	for i in range(4):
		if ipa[i] < ipb[i]:
			w_ipa,w_ipb=w_ipa+w[i],w_ipb+0
			g.append(ipb[i]-ipa[i])
		elif ipa[i] > ipb[i]:
			w_ipb,w_ipa=w_ipb+w[i],w_ipa+0
			g.append(ipa[i]-ipb[i])
		elif ipa[i] == ipb[i]:
			w_ipa,w_ipb=w_ipa+w[i],w_ipb+w[i]
			g.append(0)
	if w_ipa > w_ipb:
		return ipa,g
	elif w_ipa == w_ipb:
		return ipa,g
	elif w_ipa < w_ipb:
		return ipb,g

#ip generate
def ip_iter(seed,count):
	#print(seed,count)
	a,b,c,d=seed[0][0],seed[0][1],seed[0][2],seed[0][3]
	print("ip seed:",a,b,c,d)
	print("iter count:",count)	
	r=""
	while count > -1:
		while d < 256:
			for i in a,b,c,d:
				r+=str(i)+'.'
				#print(r)
			r=r.rstrip('.')
			#print(r,"count:",count)
			yield r
			r=""
			d+=1
			count-=1
		d=0
		if c < 256:
			c+=1
			continue
		else:
			c=0
			if b < 256:
				b+=1
				continue
			else:
				b=0
				if a < 256:
					a+=1
				else:
					print("out of ip range")
					break

if ipr:
	ip=ip_check(ipr)
	print("ip range :",ip)

	ips=set_seed(ip)
	counts=0        #the counts that how many ips need to scan
	for i in range(4):
        	counts+=ips[1][i]*256**(3-i)

	print(ips)
	print("the ip range start ",ips[0]," counts ",counts)


	ipg=ip_iter(ips,counts)
	print(ipg)

	for i in range(counts+1):
		#for i in range(6):
		#	next(ipg)
		print(next(ipg))
elif host:
	print("host ip inclue:",host)
else:
	sys.exit(0)