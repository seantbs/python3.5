#!/usr/bin/python3

from multiprocessing import Event,Queue,Pool,Process,Value
import os,time,random,threading,queue

def eq_y():
	for i in range(procs):
		if c.value > wqs:
			c.value-=wqs
			i=c.value
			yield i
		elif c.value <= wqs and c.value > int(wqs/2):
			c.value=int(c.value/2)+c.value%2
			i=c.value
			yield i

def wq_y(a,b):
	for i in range(a,b):
		i+=1
		yield i
		

def eq_put():
	print('[eq_put]',threading.current_thread().name,'prepare value...')
	g=eq_y()
	while not eq.full():
		if c.value > int(wqs/2):
			print('[eq_put]c value =',c.value)
			try:
				print('[eq_put]eq put value...')
				eq.put(next(g))
			except:
				break
		elif c.value <= int(wqs/2):
			eq.put(c.value)
			return 0
	return 1

def eq_get():
	global i
	print('[eq_get]',os.getpid(),'eq qsize:',eq.qsize())
	if not eq.empty():
		i=eq.get()
		print('[eq_get]',os.getpid(),'eq get value :',i)
		ee.set()
		wq_put()
	else:
		ee.set()
		wq_put()

def wq_put():
	global i,b
	if i >= ths:
		g=wq_y(i,b)
		while not wq.full():
			try:
				wq.put(next(g))
				i+=1
			except:
				m.get()
				break
		wfunc()
	elif i == 0:
		print('[wq_put]',threading.current_thread().name,'wq_put is done...')
		return

def pefunc():
	print(os.getpid(),'pefunc is running...')
	c_e_th()

def pwfunc():
	print(os.getpid(),'pwfunc is running...')
	c_w_th(ths)

def wfunc():
	global c_r
	while not wq.empty():
		print('[wfunc]',threading.current_thread().name,'is running code =',wq.get())
		r=random.randint(1,2)
		c_r+=r
		time.sleep(r)
	print('[wfunc]now wq is empty,wait wq put...')
	print('[wfunc]we is_set:',we.is_set())
	we.wait()
	if m.empty():
		m.put(1)
		eq_get()
	elif m.full():
		wq_put()

def efunc():
	print('[efunc]event tid',os.getpid(),'is running...')
	while True:
		if eq_put():
			we.set()
			print('[efunc]ee flag is',ee.is_set())
			ee.clear()
			ee.wait()
		elif not eq_put():
			ee.clear()
			print("[efunc]there is no c value to put eq,so pefunc done.")
			break

def c_e_th():
	print('event tid',os.getpid(),'is starting...')
	et=threading.Thread(target=efunc,name='event_tid='+str(os.getpid()))
	et.start()
	et.join()

def c_w_th(ths):
	thp=[]
	for i in range(ths):
		t=threading.Thread(target=wfunc,name='tid'+str(os.getpid())+r'/'+str(i))
		thp.append(t)
	for a in thp:
		a.start()
	for b in thp:
		b.join()

if __name__=='__main__':
	st=time.time()
#main var
	procs=2        
	#procs=os.cpu_count() 
	eq=Queue(procs)
	c=Value('i',10)
	wqs=2
#set event
	ee=Event()
	we=Event()
#start procs
	pe=Process(target=pefunc)
	pe.start()
	ths=2
	wq=queue.Queue(wqs)
	m=queue.Queue(1)
	i=0
	c_r=0
	b=10
	pw=Pool(procs)
	for i in range(procs):
		pw.apply_async(pwfunc)
	pw.close()
	pe.join()
	pw.join()

	print('real time:',c_r,'s')
	print('use time :',time.time()-st)
