#!/bin/usr/python3

import sys,time

def bar(mix,max,count,step,n):
	m='>'
	p=max/step
	if count == mix:
		sys.stdout.write('\r'+'-'*step+'0%')
		time.sleep(0.1)
	elif (count+1)%p == 0 and count+1 < max:
		n+=p
		sys.stdout.write('\r'+m*n+'-'*(step-n)+'%.2f'%(n*p/max*100)+'%')
		sys.stdout.flush()
		time.sleep(0.1)
	elif (count+1) == max:
		sys.stdout.write('\r'+'>'*step+'100.00%')
		time.sleep(0.1)
	return n

if __name__=='__main__':
	acc=0
	c=100
	for i in range(c):
		acc=bar(0,c,i,60,acc)
		
	print('\nThis is a simple propress bar test.')