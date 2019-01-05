#!/usr/bin/python3

from multiprocessing import Event,Queue,Pool,Process,Value
import os,time,random,threading,queue

def wq_y(a,b):
	for i in range(a,b):
		i*=10
		yield i
		

def eq_put():
	print('[eq_put]prepare value...')
	if c.value == 0:
		return 0
	elif c.value > 0:
		print('[eq_put]eq put value...')
		eq.put(c.value)
		c.value-=1
		return 1
	efunc()

def wq_put():
	global count,i
	if not eq.empty():
		i=eq.get()
		print('[wq_put]eq get value :',i)
		ee.set()
		print('[wq_put]ee is_set :',ee.is_set())
	if i >= 1:
		g=wq_y(i,count)
		while not wq.full():
			wq.put(next(g))
		tfunc()

def pefunc():
	print(os.getpid(),'pefunc is running...')
	c_e_th()

def pwfunc():
	print(os.getpid(),'pwfunc is running...')
	c_w_th()

def tfunc():
	while not wq.empty():
		print(threading.current_thread().name,'is code =',wq.get())
		r=random.randint(1,2)
		time.sleep(r)
	print('[tfunc]now wq is empty,wait wq put...')
	we.wait()
	wq_put()

def efunc():
	print('[efunc]event tid',os.getpid(),'is running...')
	while True:
		if eq_put():
			we.set()
			print('[efunc]ee flag is',ee.is_set())
			ee.wait()
			eq_put()
		elif not eq_put():
			print("c value = 1,so pefunc done")
			break

def c_e_th():
	print('event tid',os.getpid(),'is starting...')
	et=threading.Thread(target=efunc,name='event_tid='+str(os.getpid()))
	et.start()
	et.join()

def c_w_th():
	thp=[]
	for i in range(4):
		t=threading.Thread(target=tfunc,name='tid'+str(os.getpid())+r'/'+str(i))
		thp.append(t)
	for a in thp:
		a.start()
	for b in thp:
		b.join()

st=time.time()
wq=queue.Queue(3)
eq=Queue(1)
count=10
i=0
c=Value('i',5)
ee=Event()
ee.set()
we=Event()

pe=Process(target=pefunc)
pw=Process(target=pwfunc)
pe.start()
pw.start()
pe.join()
pw.join()

print('use time :',time.time()-st)
