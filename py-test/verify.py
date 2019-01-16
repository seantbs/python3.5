#!/usr/bin/python3

import sys,io,time,pgbar,threading,queue

def w_y():
	global allc
	for i in range(allc):
		yield i+1
		
def wq_put():
	global wg,wq
	e.clear()
	while not wq.full():
		try:
			g=next(wg)
		except:
			e.set()
			wfunc()
		wq.put(g)
	e.set()
	wfunc()

def bar():
	global n,allc
	while True:
		if n == allc:
			pgbar.bar(allc,n,60,st)
			break
		pgbar.bar(allc,n,60,st)
	print('\nbar is done....')

def wfunc():
	global n,t1,allc,wq
	while not wq.empty():
		t2=wq.get()
		r=[]
		c=0
		n+=1
		print('t2 =',t2)
		for ii in t1:
			if  t2 == ii:
				c+=1
				print('t2 =',t2)
				r.append(i)
				r.append(c)
				t3.append(r)
				allc+=1
				t1.remove(ii)
		if c == 0:
			err.append(t2)
		elif c > 1:
			err.append(t2)
	if n+1 <= allc:
		e.wait()
		wq_put()
	elif n+1 > allc:
		return
	#print(threading.current_thread().name, 'is done...')

if __name__=='__main__':
	st=time.time()
	print('\nrunning:')
	fname='result.log'
	f=open('./'+fname,'r+')
	t1=f.readlines()
	t3=[]
	allc=len(t1)
	print(fname,'lines =',allc)
	err=[]
	n=0
	wg=w_y()

	ths=10
	wq=queue.Queue(ths)
	thp=[]
	e=threading.Event()
	e.set()
	#et=threading.Thread(target=wfunc,name='tid'+str(i))
	for i in range(ths):
		t=threading.Thread(target=wfunc,name='tid'+str(i))
		thp.append(t)
	#bar=threading.Thread(target=bar,name='tid-bar')
	#bar.start()
	for a in thp:
		a.start()
	for b in thp:
		b.join(2)
	#bar.join(2)


	print('\nt1 count:',len(t1),'\nt3 count:',len(t3),'\nerr count:',len(err),'\n')
	print('use time :',time.time()-st,'s')
