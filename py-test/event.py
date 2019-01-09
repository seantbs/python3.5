#!/usr/bin/python3

from multiprocessing import Event,Queue,Pool,Process,Value
import os,time,random,threading,queue

def eq_y(a,b,c):
	for i in range(c):
		if a > b:
			a-=b
			yield a
		elif a <= b:
			a=int(a/2)+a%2
			yield a
		elif a ==1:
			yield a

def wq_y(a,b):
	for i in range(a,b):
		yield i

def eq_put():
	global task,wqs,procs,eq
	#print('[eq_put]',threading.current_thread().name,'prepare value...')
	while not eq.full():
		if task > 1:
			g=eq_y(task,wqs,procs)
			#print('[eq_put]task =',task)
			try:
				#print('[eq_put]eq put value...')
				task=next(g)
				#print('[eq_put]eq put value =',task)
				eq.put(task)
			except:
				break
		elif task == 1:
			#print('[eq_put]if task is 1 =',task)
			eq=Queue(1)
			eq.put(task)
			return 0
	return 1

def eq_get():
	global i
	#print('[eq_get]',os.getpid(),'eq qsize:',eq.qsize())
	if not eq.empty() and i != None:
		i=eq.get()
		if i > 1:
			#print('[eq_put]ee set:',ee.is_set(),'we set:',we.is_set())
			ee.set()
			we.set()
			wq_put()
		elif i == 1:
			we,set()
			wq_put()

def wq_put():
	global i,b
	x=0
	#print('[wq_put]',threading.current_thread().name,'i =',i)
	if i:
		if i > 1:
			g=wq_y(i,i+wqs)
			while not wq.full():
				try:
					x=next(g)
					#print('[wq_put]',threading.current_thread().name,'next g =',x)
					wq.put(x)
				except:
					break
			try:
				m.get_nowait()
			except:
				pass
			wfunc()
		elif i == 1:
			wq.put(1)
			i=None
			wfunc()

def pefunc():
	print(os.getpid(),'pefunc is running...')
	c_e_th()

def pwfunc():
	print(os.getpid(),'pwfunc is running...')
	c_w_th(ths)

def wfunc():
	while not wq.empty():
		print('[wfunc]',threading.current_thread().name,'is running code =\t',wq.get())
		r=random.randint(1,2)
		cr.value+=r
		count.value+=1
		time.sleep(r)
	#print('[wfunc]',threading.current_thread().name,'now wq is empty,wait wq put...')
	we.wait()
	if not m.full() and i != None:
		try:
			m.put_nowait(threading.current_thread().name)
			eq_get()
		except:
			we.clear()
			we.wait()
			wq_put()

def efunc():
	x=None
	print('[efunc]event tid',os.getpid(),'is running...')
	while True:
		x=eq_put()
		#print('[efunc]eq_put is',x)
		if x:
			we.set()
			ee.clear()
			ee.wait()
		elif not x:
			print("[efunc]there is no more task put to eq,so pefunc done.")
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
	task=10000
	wqs=100
#set event
	ee=Event()
	ee.set()
	we=Event()
#start procs
	pe=Process(target=pefunc)
	pe.start()
	ths=200
	wq=queue.Queue(wqs)
	m=queue.Queue(1)
	i=0
	cr=Value('i',0)
	count=Value('i',0)
	pw=Pool(procs)
	for i in range(procs):
		pw.apply_async(pwfunc)
	pw.close()
	pe.join()
	pw.join()

	print('real time:',cr.value,'s\tcounts:',count.value)
	print('use time :',time.time()-st,'s')
