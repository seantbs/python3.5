#!/bin/usr/python3

import sys,time

def utime(st):
	sec=int(time.time()-st)
	cs=sec%60
	min=int(sec/60)
	cm=min%60
	hour=int(min/60)
	if cs < 60 and cm < 60:
		return '%02i:%02i:%02i' % (hour,cm,cs)
	elif cs == 0:
		return '%02i:%02i:00' % (hour,cm)

def bar(max,count,step,st):
	m='>'
	p=max/step
	r=100/step
	a=count
	c=a/p
	if c/r >= 1 and a < max:
		sys.stdout.write('\r'+m*int(c)+'-'*(step-int(c))+'%.2f'%(c*p/max*100)+'%'+'   '+str(utime(st)))
		sys.stdout.flush()
	elif a >= max:
		sys.stdout.write('\r'+m*step+'100.00%'+'   '+str(utime(st)))
		sys.stdout.flush()

def ratio(max,count,step):
	if count%step == 0:
		sys.stdout.write('\r'+str(count)+'/'+str(max)+'   '+str(utime(st)))
		sys.stdout.flush()
	elif count == max:
		sys.stdout.write('\r'+str(count)+'/'+str(max)+'   '+str(utime(st)))
		sys.stdout.flush()

if __name__=='__main__':
	st=time.time()
	c=65535
	print('\nThis is a simple propress bar test.')
	for i in range(c):
		i+=1
		bar(c,i,60,st)
		#ratio(c,i,60,st)
		time.sleep(0.001)
	print('\n')
