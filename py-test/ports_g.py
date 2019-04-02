#!/usr/bin/python3.5

import sys,os,time,argparse

def check_value(args):
	id=0
	err=[]
	for i in args:
		id+=1
		if type(i) == int:
			if i > -1 and i < 65536:
				continue
			else:
				err.append('value:'+str(i)+' -> list_id:'+str(id))
				print('port setting error',err)
				sys.exit(0)
		else:
			err.append(str(i)+" -> check_id:"+str(id))
			print('port setting error',err)
			sys.exit(0)

#check port must be 0-65535
def check_p(*args):
	#print(type(args[0]))
	if type(args[0]) == int:
		check_value(args)
		return 1
	elif type(args[0]) == list:
		check_value(args[0])
		return 1
	return 0

#port range generate
def port_range(s,e):
	if s > e:
		print("warn:-ps value must less than -pe value.please check -pe default value.")
		sys.exit(0)
		
	while s <= e:
		yield s
		s=s+1

#specify port func
def port_list(sp):
	for i in sp:
		yield i

if __name__=='__main__':
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

	#test pg
	if check_p(sp):
		print('sp :',type(sp))
		g=port_list(sp)
		for i in g:
			print('port list:',i)
	elif check_p(ps,pe):
		scan=port_range(ps,pe)
		for i in scan:
			print("scan port range:",i)
	else:
		print("port setting error!please check the input...")
		sys.exit(0)
