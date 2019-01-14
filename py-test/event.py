#!/usr/bin/python3

from multiprocessing import Event,Queue,Pool,Process,Value
import io,os,sys,time,random,threading,queue

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
				if a > c:
					a=a-(int(a/c)+a%c)
					yield a
				elif a < c:
					yield 0
			elif a*c < b:
					yield 0

def wq_put_y(a,b):
	for i in range(a,b):
		i+=1
		yield i

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
			#print('[eq_put]eq put value =',task)
			#print('[eq_put]eql :',eql)
			eq.put(eql)
		elif task == 0:
			eql.append(0)
			#print('[eq_put]eq put value =',task)
			#print('[eq_put]eql :',eql)
			eq.put(eql)
			#print('[eq_put]eq put value = 0,so eq_put done.')
			return 0
	return 1

def eq_get():
	global wqs,wg,procs
	wq=[]
	wql=None
	wqn=None
	we.clear()
	if not eq.empty():
		wq=eq.get()
		wql=wq.pop(0)
		wqn=wq.pop(0)
		ee.set()
		wg=wq_put_y(wqn,wql)
		#print('[eq_get]',threading.current_thread().name,'wqn >= wqs*procs wql =',wql)
		#print('[eq_get]',threading.current_thread().name,'wqn >= wqs*procs wqn =',wqn)
		we.set()
		wq_put()
	else:
		print('[eq_get]eq is empty',threading.current_thread().name,'wqn =',wqn)
		we.set()
		wq_put()

def wq_put():
	global wg
	x=None
	#print('[wq_put]',threading.current_thread().name,'wqn =',wqn,'wql =',wql)
	if not wq.full():
		try:
			x=next(wg)
			wq.put(x)
		except:
			if not m.empty():
				m.get()
		wfunc()
	else:
		wfunc()

def wfunc():
	global ptime,pcount,ramf
	while not wq.empty():
		#ramf.write(threading.current_thread().name+' is running code =\t'+str(wq.get())+'\n')
		ramf.write(str(wq.get())+'\n')
		#print('[wfunc]',threading.current_thread().name,'is running code =\t',wq.get())
		r=random.randint(1,2)
		ptime+=r
		pcount+=1
		time.sleep(r)
	#print('[wfunc]',threading.current_thread().name,'now wq is empty,wait wq put...')
	if not m.full() and not eq.empty():
		if not m.full():
			m.put(threading.current_thread().name)
			eq_get()
		else:
			we.wait()
			wq_put()
	elif m.empty() and eq.empty():
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
			print("[efunc]there is no more task put to eq,so efunc done.")
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
		b.join(4)
	#print('[wfunc]',os.getpid(),'wfunc is done...')

def pefunc():
	print(os.getpid(),'pefunc is running...')
	c_e_th()

def pwfunc():
	global allcount,alltime,reslog,ramf
	print(os.getpid(),'pwfunc is running...')
	c_w_th(ths)
	ramf2=io.StringIO(ramf.getvalue())
	allcount.value+=pcount
	alltime.value+=ptime
	print('pid =',os.getpid(),'real time:',ptime,'s\tcounts:',pcount)
	while True:
		ram2res=ramf2.readline()
		if ram2res == '':
			break
		try:
			reslog.write(ram2res)
			reslog.flush()
		except:
			print('result.log write erroe at line:',ram2res)
			continue

if __name__=='__main__':
	st=time.time()
#main public var
	try:
		os.remove('./result.log')
	except:
		pass
	os.path.exists("./result.log")
	reslog=open('./result.log','a+')
	ramf=io.StringIO()
	procs=4
	ths=1024
	#procs=os.cpu_count()
	eq=Queue(procs)
	task=50000
	wqs=ths*4
#set event of procs
	ee=Event()
	ee.set()
#set var in procs
	pe=Process(target=pefunc)
	pe.start()
	wq=queue.Queue(wqs)
	m=queue.Queue(1)
	we=threading.Event()
	wg=None
	ptime=0
	pcount=0
	alltime=Value('i',0)
	allcount=Value('i',0)
	pw=Pool(procs)
	for i in range(procs):
		pw.apply_async(pwfunc)
	pw.close()
	pe.join()
	pw.join()
	reslog.close()
	print('real time:',alltime.value,'s\tcounts:',allcount.value)
	print('use time :',time.time()-st,'s')
