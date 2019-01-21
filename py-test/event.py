#!/usr/bin/python3.5

from multiprocessing import Event,Queue,Pool,Process,Value
import io,os,sys,time,random,threading,queue,pgbar

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
			elif a*c >= b/c and a < b*c:
				if a > c:
					a=a-(int(a/c)+a%c)
					yield a
				elif a < c:
					yield 0
			elif a*c < b/c:
					yield 0

def wq_put_y(a,b):
	for i in range(a,b):
		yield i+1

def eq_put():
	global task,wqs,procs
	#print('[eq_put]',threading.current_thread().name,'prepare value...')
	g=eq_put_y(task,wqs,procs)
	while not eq.full():
		eql=[]
		#print('[eq_put]task =',task)
		eql.append(task)
		task=next(g)
		if task != 0:
			eql.append(task)
			#print('[eq_put]eql :',eql)
			eq.put(eql)
		elif task == 0:
			eql.append(0)
			#print('[eq_put]eql :',eql)
			eq.put(eql)
			return 0
	return 1

def eq_get():
	global wqs,wg,procs,weqget
	wqe=[]
	wqa=None
	wqb=None
	print(threading.current_thread().name,'weqget =',weqget)
	if weqget:
		while eq.empty():
			print(threading.current_thread().name,'ee set',ee.is_set())
			if ee.is_set():
				continue
			else:
				break
	else:
		we.set()
		wfunc()
		return

	if not eq.empty():
		wqe=eq.get()
		print('wqe =',wqe)
		if wqe != None:
			weqget=True
			#print('[eq_get]wqe =',wqe)
			wqa=wqe.pop()
			wqb=wqe.pop()
			wg=wq_put_y(wqa,wqb)
			ee.set()
			we.set()
			wq_put()
		elif wqe == None:
			weqget=False
			print(threading.current_thread().name,'None weqget =',weqget)
			#a=wcq.get()
			#print('[eq_get]eq is empty :',threading.current_thread().name)
			ee.clear()
			we.set()
			wfunc()

def wq_put():
	global wg,weqget
	x=None
	try:
		x=next(wg)
	except:
		if not wcq.empty() and weqget:
			a=wcq.get()
			print('wcq get =',a)
			wfunc()
			return
		elif not weqget:
			wfunc()
			return
	if not wq.full() and x != None:
		wq.put(x)
		wfunc()
	else:
		wfunc()

def wfunc():
	global ptime,pcount,ramf,weqget
	a=None
	n=0
	while not wq.empty():
		a=wq.get()
		#print('a =\t',a)
		std=str(a)+'\n'
		ramf.write(std)
		#print('[wfunc]',threading.current_thread().name,'is running code =\t',wq.get())
		r=random.randint(2,5)
		ptime+=r
		pcount+=1
		time.sleep(r)
		n+=1
	if wcq.empty() and weqget:
		wcq.put_nowait(threading.current_thread().name)
		we.clear()
		eq_get()
	elif wcq.full() and not weqget:
		print('wcq empty',wcq.empty(),'weqget =',weqget)
		return
	else:
		we.wait()
		wq_put()

def efunc():
	print('[efunc]event tid',os.getpid(),'is running...')
	while True:
		x=None
		x=eq_put()
		if x:
			ee.clear()
			ee.wait()
		else:
			ee.clear()
			eq.put(None)
			break

def wfunc_bar():
	global bartask,st
	while True:
		count=bar.value
		if count < bartask:
			pgbar.bar(bartask,count,50,st)
		elif count >= bartask:
			pgbar.bar(bartask,count,50,st)
			ee.set()
			break
		#print('count =',count)
		time.sleep(0.01)

def c_e_th():
	print('event tid',os.getpid(),'is starting...')
	et=threading.Thread(target=efunc,name='event_tid='+str(os.getpid()))
	#wbar=threading.Thread(target=wfunc_bar,name='wbar_tid='+str(os.getpid()))
	et.start()
	#wbar.start()
	et.join()
	#wbar.join()
	print('\n[efunc]there is no more task so efunc done.use time:%.2f' % (time.time()-st)+'s')
	print('='*60+'\n')
	print('waiting for wfunc thread over...')

def c_w_th(ths):
	thp=[]
	for i in range(ths):
		t=threading.Thread(target=wfunc,name='tid'+str(os.getpid())+r'/'+str(i))
		thp.append(t)
	for a in thp:
		a.start()
	for b in thp:
		b.join()

def pefunc():
	print(os.getpid(),'pefunc is running...')
	c_e_th()

def pwfunc():
	global allcount,alltime,reslog,ramf
	print('[pwfunc]pid =',os.getpid(),'is running...')
	c_w_th(ths)
	allcount.value+=pcount
	alltime.value+=ptime
	ramf2=io.StringIO(ramf.getvalue())
	while True:
		ram2res=ramf2.readline()
		if ram2res == '':
			break
		try:
			reslog.write(ram2res)
		except:
			print('test.log write erroe at line:',ram2res)
			continue
	reslog.flush()
	ramf2.close()
	print('\npid ='+str(os.getpid())+' real time: '+str(ptime)+'s\tcounts:'+str(pcount))
	print('[wfunc]'+str(os.getpid())+' wfunc is done use time:%.2f' % (time.time()-st)+'s')

if __name__=='__main__':
	st=time.time()

#main public var
	fname='./result.log'
	try:
		os.remove(fname)
	except:
		pass
	os.path.exists(fname)

	procs=1
	ths=7969
	wqs=int(ths/procs)
	#procs=os.cpu_count()
	eq=Queue(procs)
	task=10000
	bartask=task
	alltime=Value('i',0)
	allcount=Value('i',0)
	bar=Value('i',1)

#set var to event procs
	ee=Event()
	pe=Process(target=pefunc)
	pe.start()

#set var to work procs
	reslog=open(fname,'a+')
	ramf=io.StringIO()
	wq=queue.Queue(wqs)
	wcq=queue.Queue(1)
	we=threading.Event()
	weqget=True
	wg=None
	ptime=0
	pcount=0
	pw=Pool(procs)
	for i in range(procs):
		pw.apply_async(pwfunc)
	pw.close()
	pe.join()
	pw.join()
	ramf.close()
	reslog.close()
	print('\nreal time: '+str(alltime.value)+'s\tcounts: '+str(allcount.value))
	print('use time: %.2f' % (time.time()-st)+'s')