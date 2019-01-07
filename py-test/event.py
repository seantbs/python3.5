#!/usr/bin/python3

from multiprocessing import Event,Queue,Pool,Process,Value
import os,time,random,threading,queue

def eq_y(a):
	for i in range(a):
		if a >= wqs:
			i=c.value-wqs
			c.value=i
			yield i
		if c.value < wqs and c.value >0:
			yield c.value

def wq_y(a,b):
	for i in range(a,b):
		i+=1
		yield i
		

def eq_put():
	print('[eq_put]prepare value...')
	if c.value < 0:
		return 0
	elif c.value >= 0:
		g=eq_y(c.value)
		while not eq.full():
			try:
				print('[eq_put]eq put value...')
				eq.put(next(g))
			except:
				break
		return 1

def eq_get():
	global i
	if not eq.empty():
		i=eq.get()
		print('[eq_get]',os.getpid(),'eq get value :',i)
		ee.set()
		#print('[eq_get]ee is_set :',ee.is_set())
		wq_put()

def wq_put():
	global i
	if i > 0:
		g=wq_y(i-ths,i)
		while not wq.full():
			try:
				wq.put(next(g))
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
	mark=None
	c_w_th(ths)

def wfunc():
	while not wq.empty():
		print('[wfunc]',threading.current_thread().name,'is running code =',wq.get())
		r=random.randint(1,2)
		c_r+=r
		time.sleep(r)
	print('[tfunc]now wq is empty,wait wq put...')
	we.wait()
	if m.empty():
		m.put(False)
		eq_get()
	elif m.full():
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
			ee.clear()
			print("c value = 0,so pefunc done")
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
	c=Value('i',20)
#set event
	ee=Event()
	we=Event()
#start procs
	pe=Process(target=pefunc)
	pe.start()
	ths=4
	wqs=4
	wq=queue.Queue(wqs)
	m=queue.Queue(1)
	i=0
	pw=Pool(procs)
	for i in range(procs):
		pw.apply_async(pwfunc)
	pw.close()
	pe.join()
	pw.join()

print('use time :',time.time()-st)
