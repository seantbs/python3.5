#!/usr/bin/python3

from multiprocessing import Event,Queue,Pool,Process,Value
import os,time,random,threading,queue

def eq_put_y(a,b,c):
	if a == 0:
		return
	if c == 1:
		for i in range(c):
			if a >= b:
				a-=b
				yield a
			else:
				yield 0
	elif c > 1:
		for i in range(c):
			if a >= b*c:
				a-=b
				yield a
			elif a*c >= b and a < b*c:
				a=a-(int(a/c)+a%c)
				yield a
			elif a*c < b:
				yield 0

def wq_put_y(a,b):
	for i in range(a,b):
		yield i

def eq_put():
	global task,wqs,procs
	print('[eq_put]',threading.current_thread().name,'prepare value...')
	if task*procs > wqs:
		g=eq_put_y(task,wqs,procs)
		while not eq.full():
			print('[eq_put]task =',task)
			task=next(g)
			print('[eq_put]eq put value =',task)
			eq.put(task)
	else:
		print('[eq_put]eq put value = 0,so eq_put done.')
		return 0
	return 1		

def eq_get():
	global wqs,wql,wqn,wg,procs
	we.clear()
	if not eq.empty():
		wqn=eq.get()
		ee.set()
		if wqn+wqs >= wqs*procs:
			wg=wq_put_y(wqn,wqn+wqs)
			#print('[eq_get]',threading.current_thread().name,'wqn >= wqs*procs wql =',wql)
			wql=wqn
			print('[eq_get]',threading.current_thread().name,'wqn >= wqs*procs wqn =',wqn)
			we.set()
			wq_put()
		elif wqn*procs >= wqs and wqn < wqs*procs:
			wg=wq_put_y(5,10)
			#print('[eq_get]',threading.current_thread().name,'wqn > wqs and wqn < wqs*procs wql =',wql)
			wql=wqn
			print('[eq_get]',threading.current_thread().name,'wqn > wqs and wqn < wqs*procs wqn =',wqn)
			we.set()
			wq_put()
		elif wqn*procs < wqs:
			wg=wq_put_y(0,5)
			print('[eq_get]',threading.current_thread().name,'wqn is 0,so eq_get done.')
			we.set()
			wq_put()
	else:
		print('[eq_get]eq is empty',threading.current_thread().name,'wqn =',wqn)
		we.set()
		wq_put()

def wq_put():
	global wg
	print('[wq_put]',threading.current_thread().name,'we is set =',we.is_set())
	x=None
	#print('[wq_put]',threading.current_thread().name,'wqn =',wqn,'wql =',wql)
	if not wq.full():
		try:
			x=next(wg)
			#print('[wq_put]',threading.current_thread().name,'next g =',x)
			wq.put(x)
		except:
			#print('[wq_put]m is getting...')
			if not m.empty():
				m.get()
		wfunc()
	else:
		wfunc()

def wfunc():
	global cr,count
	while not wq.empty():
		print('[wfunc]',threading.current_thread().name,'is running code =\t',wq.get())
		r=random.randint(1,2)
		cr+=r
		count+=1
		time.sleep(r)
	#print('[wfunc]',threading.current_thread().name,'now wq is empty,wait wq put...')
	if not m.full() and not eq.empty():
		if not m.full():
			m.put(threading.current_thread().name)
			#print('[wfunc]',threading.current_thread().name,'m put...')
			eq_get()
		else:
			#print('[wfunc]',threading.current_thread().name,'wfunc elifis wait...')
			#print('[wfunc]elifis',threading.current_thread().name,'we is set =',we.is_set())
			we.wait()
			wq_put()
	elif m.empty() and eq.empty():
		return
	else:
		#print('[wfunc]',threading.current_thread().name,'wfunc else is wait...')
		#print('[wfunc]else',threading.current_thread().name,'we is set =',we.is_set())
		we.wait()
		wq_put()

def efunc():
	print('[efunc]event tid',os.getpid(),'is running...')
	while True:
		x=None
		x=eq_put()
		if x:
			print('[efunc]eq_put is',x)
			ee.clear()
			ee.wait()
		else:
			print('[efunc]eq_put is',x)
			print("[efunc]there is no more task put to eq,so pefunc done.")
			print('*'*60)
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
	print('[wfunc]',os.getpid(),'wfunc is done...')

def pefunc():
	print(os.getpid(),'pefunc is running...')
	c_e_th()

def pwfunc():
	print(os.getpid(),'pwfunc is running...')
	c_w_th(ths)		
	print('pid =',os.getpid(),'real time:',cr,'s\tcounts:',count)

if __name__=='__main__':
	st=time.time()
#main public var
	procs=2
	#procs=os.cpu_count()
	eq=Queue(procs)
	task=10
	wqs=8
#set event of procs
	ee=Event()
	ee.set()
#set var in procs
	pe=Process(target=pefunc)
	pe.start()
	ths=16
	wq=queue.Queue(wqs)
	m=queue.Queue(1)
	we=threading.Event()
	wql=0
	wqn=0
	wg=None
	cr=0
	count=0
	pw=Pool(procs)
	for i in range(procs):
		pw.apply_async(pwfunc)
	pw.close()
	pe.join()
	pw.join()
	#print('pid =',os.getpid(),'real time:',cr,'s\tcounts:',count)
	print('use time :',time.time()-st,'s')
