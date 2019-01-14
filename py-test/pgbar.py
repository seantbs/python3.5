#!/bin/usr/python3

import sys,time

def bar(max,count,step):
	m='>'
	p=max/step
	n=0
	if (count+1)/p > 1:
		n=int((count+1)/p)
		sys.stdout.write('\r'+m*n+'-'*(step-n)+'%.2f'%(n*p/max*100)+'%')
		time.sleep(0.01)

if __name__=='__main__':
	acc=0
	c=100
	for i in range(c):
		bar(c,i,50)
		
	print('\nThis is a simple propress bar test.')