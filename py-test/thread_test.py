#!/usr/bin/python3.5

import os,io,sys,queue,threading,time,random

stime=time.time()

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

def pq_get():
	global pq,a
	#print("pq_get func a =",a)
	while not pq.empty():
		print(threading.current_thread().name,"is running code =\t",pq.get())
		time.sleep(random.randint(1,2))
	pq_put()

if __name__=='__main__':
	a=1
	b=1001
	ths=100
	pq=queue.Queue(ths)
	
	thp=[]
	for i in range(ths):
		t=threading.Thread(target=pq_get,args=(),name="threadid-"+str(i))
		thp.append(t)
	for c in thp:
		c.start()
	for d in thp:
		d.join()

	print("real time:",time.time()-stime)
