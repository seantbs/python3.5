#!/usr/bin/python3

import sys,os,time,argparse

parser=argparse.ArgumentParser(description='input port range with int.default scan ports 1-1024.')
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
parser.add_argument('-ps',type=int,nargs='?',default=1,help='set start port vaule')
parser.add_argument('-pe',type=int,nargs='?',default=1024,help='set end port vaule')
parser.add_argument('-sp',type=int,nargs='+',help="set specify port vaule like '80 135 137'")
parser.parse_args()
args=parser.parse_args()

ps=args.ps
pe=args.pe
sp=args.sp
print("ps=",ps)
print("pe=",pe)
print("sp=",sp)

#check port must be 0-65535
def check_p(*args):
	id=0
	err=[]

	for i in args:
		if type(i) == int:
			if i > -1 and i < 65536:
				i=i
			else:
				err.append(str(i)+" -> check_id:"+str(id))
		elif type(i) == list:
			if i[0]!=None:
				print(i[0]!=None)
				for e in i:
					print(e)
					if e > -1 and e < 65536:
						i=i
					else:	
						err.append(str(e)+" -> check_id:"+str(id))
		else:
			return 0
		id+=1
	if len(err) == 0:
		return 1
	elif len(err) != 0:
		print(err,"are not Correct port numbers or range be Detected, will use default setting")
		sys.exit(0)

#port range generate
def prange(s,e):
	if s > e:
		print("warn:-ps value must less than -pe value.please check -pe default value.")
		sys.exit(0)
		
	while s <= e:
		yield s
		s=s+1

#specify port func
def plist(a):
	for i in a:
		print("scan sp port:",i)



#test pg
if check_p(sp):
	plist(sp)
elif check_p(ps,pe):
	scan=prange(ps,pe)
	for i in scan:
        	print("scan port range:",i)
else:
	print("please input port numbers or range")
	sys.exit(0)