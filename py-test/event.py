#!/usr/bin/python3

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
			#print('[eq_put]eql :',eql)
			eq.put(eql)
		elif task == 0:
			eql.append(0)
			#print('[eq_put]eql :',eql)
			eq.put(eql)
			#print('[eq_put]eq put value = 0,so eq_put done.')
			return 0
	return 1

def eq_get():
	global wqs,wg,procs
	wqe=[]
	wqa=None
	wqb=None
	we.clear()
	if not eq.empty():
		wqe=eq.get()
		#print('[eq_get]wqe =',wqe)
		wqa=wqe.pop()
		wqb=wqe.pop()
		ee.set()
		wg=wq_put_y(wqa,wqb)
		we.set()
		wq_put()
	else:
		#print('[eq_get]eq is empty :',threading.current_thread().name)
		we.set()
		wfunc()

def wq_put():
	global wg
	x=None
	try:
		x=next(wg)
	except:
		if not m.empty():
			m.get()
		wfunc()
		
	if not wq.full() and x != None:
		wq.put(x)
		wfunc()
	else:
		wfunc()

def wfunc():
	global n,ptime,pcount,ramf
	n=0
	while not wq.empty():
		std=str(wq.get())+'\n'
		ramf.write(std)
		#print('[wfunc]',threading.current_thread().name,'is running code =\t',wq.get())
		r=random.randint(3,5)
		ptime+=r
		pcount+=1
		time.sleep(r)
		n+=1
	
	#print('[wfunc]',threading.current_thread().name,'now wq is empty,wait wq put...')
	if not m.full() and not eq.empty():
		if not m.full():
			m.put(threading.current_thread().name)
			eq_get()
		else:
			bar.value+=n
			we.wait()
			wq_put()
	elif m.empty() and eq.empty():
		#print('m and eq queue is empty so wfunc done.')
		if not ee.is_set():
			we.clear()
		elif ee.is_set():
			we.set()
		bar.value+=n
		we.wait()
		return
	else:
		bar.value+=n
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
		time.sleep(0.2)

def c_e_th():
	print('event tid',os.getpid(),'is starting...')
	et=threading.Thread(target=efunc,name='event_tid='+str(os.getpid()))
	wbar=threading.Thread(target=wfunc_bar,name='wbar_tid='+str(os.getpid()))
	wbar.start()
	et.start()
	et.join()
	wbar.join()
	print('\n[efunc]there is no more task so efunc done.use time:%.2f' % (time.time()-st)+'s')
	print('*'*60+'\n')
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
	n=0
	c_w_th(ths)
	ramf2=io.StringIO(ramf.getvalue())
	allcount.value+=pcount
	alltime.value+=ptime
	print('\npid ='+str(os.getpid())+' real time: '+str(ptime)+'s\tcounts:'+str(pcount))
	print('[wfunc]'+str(os.getpid())+' wfunc is done use time:%.2f' % (time.time()-st)+'s')
	while True:
		ram2res=ramf2.readline()
		n+=1
		if ram2res == '':
			break
		try:
			reslog.write(ram2res)
		except:
			print('test.log write erroe at line:',ram2res)
			continue
		reslog.flush()

if __name__=='__main__':
	st=time.time()
#main public var
	try:
		os.remove('./test.log')
	except:
		pass
	os.path.exists("./test.log")
	reslog=open('./test.log','a+')
	ramf=io.StringIO()
	procs=4
	ths=2048
	wqs=ths*2
	#procs=os.cpu_count()
	eq=Queue(procs)
	task=655350
	bartask=task
	alltime=Value('i',0)
	allcount=Value('i',0)
	bar=Value('i',1)
#set event
	ee=Event()
	ee.set()
#set var to procs
	pe=Process(target=pefunc)
	pe.start()
	wq=queue.Queue(wqs)
	m=queue.Queue(1)
	we=threading.Event()
	wg=None
	ptime=0
	pcount=0
	pw=Pool(procs)
	for i in range(procs):
		pw.apply_async(pwfunc)
	pw.close()
	pe.join()
	pw.join()
	reslog.close()
	print('\nreal time: '+str(alltime.value)+'s\tcounts: '+str(allcount.value))
	print('use time: %.2f' % (time.time()-st)+'s')
