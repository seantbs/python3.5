#!/bin/usr/python3

import sys,time

def bar(max,count,step):
	m='>'
	p=max/step
	r=100/step
	n=0
	a=count
	c=a/p
	if c >= r and a < max:
		n=c/r
		sys.stdout.write('\r'+m*int(n)+'-'*(step-int(n))+'%.2f'%(n*p/max*100)+'%'+'='+str(a))
		sys.stdout.flush()
	elif a == max:
		sys.stdout.write('\r'+m*step+'100.00%'+'='+str(a))
		sys.stdout.flush()

def ratio(max,count,step):
	if count%step == 0:
		sys.stdout.write('\r'+str(count)+'/'+str(max))
		sys.stdout.flush()
	elif count == max:
		sys.stdout.write('\r'+str(count)+'/'+str(max))
		sys.stdout.flush()
	
if __name__=='__main__':
	acc=0
	c=10000
	print('\nThis is a simple propress bar test.')
	for i in range(c):
		i+=1
		#bar(c,i,60)
		ratio(c,i,75)
		time.sleep(0.001)
	print('\n')