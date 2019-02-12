#!/usr/bin/python3

import os,io,sys,queue,threading,time,random
from memory_profiler import profile

def y(s,e):
	global a
	#print("y func a =",a)
	if s == a:
		a=a+1
		for i in range(s,e):
			yield i
	else:
		pg_put()

def pq_put():
	global pq,a,b
	for i in range(a,b):
		g=y(i,i+1)
		try:
			 pq.put(next(g))
		except:
			break
		#print("pq func a =",a)

#@profile(precision=4)
def pq_get():
	global pq,a,tcount,wcount
	#print("pq_get func a =",a)
	while not pq.empty():
		print(threading.current_thread().name,"is running code =\t",pq.get())
		rtime=random.randint(2,6)
		time.sleep(rtime)
		tcount+=rtime
		wcount+=1
	pq_put()

if __name__=='__main__':
	st=time.time()
	a=1
	ths=int(input('set thread count:'))
	b=int(input('set task count:'))
	b+=1
	tcount=0
	wcount=0
	
	pq=queue.Queue(ths)
	
	thp=[]
	for i in range(ths):
		t=threading.Thread(target=pq_get,args=(),name="threadid-"+str(i))
		thp.append(t)
	for c in thp:
		c.start()
	for d in thp:
		d.join()

	print('\nreal time: '+str(tcount)+'s\tcounts: '+str(wcount))
	print('use time: %.2f' % (time.time()-st)+'s')