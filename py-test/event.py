#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

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
	eg=eq_put_y(task,wqs,procs)
	while not eq.full():
		eql=[]
		#print('[eq_put]task =',task)
		eql.append(task)
		task=next(eg)
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
	#print(threading.current_thread().name,'weqget =',weqget,'ee set',ee.is_set())

	while eq.empty():
		if weqget and ee.is_set():
			print('eq_get]',threading.current_thread().name,'weqget is true ee set',ee.is_set())
			continue
		elif not ee.is_set():
			break
		elif not weqget:
			we.set()
			wfunc()
			return

	if not eq.empty() and weqget:
		wqe=eq.get()
		print('[eq_get]',threading.current_thread().name,'wqe =',wqe,'we set',we.is_set())
		if wqe != None:
			#print('[eq_get]wqe =',wqe)
			wqa=wqe.pop()
			wqb=wqe.pop()
			wg=wq_put_y(wqa,wqb)
			ee.set()
			we.set()
			wq_put()
		elif wqe == None:
			weqget=False
			print('[eq_get]',threading.current_thread().name,'wcq empty',wcq.empty(),'none ee set:',ee.is_set())
			ee.set()
			we.set()
			wfunc()
	elif not eq.empty() and not weqget:
		we.set()
		wfunc()

def wq_put():
	global wg,weqget
	x=None
	try:
		x=next(wg)
	except:
		if not wcq.empty() and weqget:
			we.clear()
			wcq.get_nowait()
			wfunc()
			return
		else:
			we.clear()
			wfunc()
			return

	#print('[wq_put]',threading.current_thread().name,'x =',x,'we set',we.is_set())
	if not wq.full():
		wq.put_nowait(x)
		wfunc()
	else:
		wfunc()

def wfunc():
	global ptime,pcount,resbf,threadover,weqget
	x=None
	n=0
	while not wq.empty():
		text=''
		x=wq.get_nowait()
		r=random.randint(2,6)
		for i in range(r):
			text+='a'
			time.sleep(1)
		std=str(x)+'\t'+text+'\n'
		resbf.put_nowait(std)
		ptime+=r
		pcount+=1
		n+=1

	if wcq.empty() and weqget:
		try:
			wcq.put_nowait(threading.current_thread().name)
		except:
			wfunc()
		#print('[wfunc]',threading.current_thread().name,'wcq empty',wcq.empty(),'we set',we.is_set())
		eq_get()
	elif not weqget and not wcq.empty():
		#print('[wfunc]',threading.current_thread().name,'is wait to done...','we set',we.is_set())
		#we.clear()
		#we.wait()
		return
	else:
		#print('[wfunc]',threading.current_thread().name,'wq is empty we set',we.is_set())
		we.wait(2)
		wq_put()

def efunc():
	global procs
	print('[efunc]event tid',os.getpid(),'is running...')
	while True:
		x=None
		x=eq_put()
		if x:
			ee.clear()
			ee.wait()
			et.set()
		else:
			et.clear()
			break
	n=0
	while True:
		if not eq.full():
			n+=1
			print('[efunc]n =',n,'eq empty',eq.empty())
			if n <= procs:
				eq.put(None)
			elif n > procs and eq.empty():
				ee.clear()
				et.set()
				return
		ee.clear()
		ee.wait()

def resbf_flush():
	global resbf,reslog,errline,task,procs
	et.clear()
	while True:
		et.wait()
		resbfqs=resbf.qsize()
		#print('[resbf_flus]task!=0,resbf qsize =',resbfqs)
		if resbfqs >= procs:
			thqs=int((resbfqs-resbfqs%procs)/procs)
		else:
			thqs=resbfqs
		#print('[resbf_flus]task!=0,thqs =',thqs)
		for i in range(thqs):
			errline+=1
			try:
				v=resbf.get_nowait()
			except:
				break
			try:
				reslog.write(v)
			except:
				print('reslog write erroe at line:',errline,v)
				continue
		reslog.flush()
		if task != 0:
			et.clear()
			continue
		else:
			#print('[resbf_flush]1 et set:',et.is_set(),'ee set:',ee.is_set())
			et.wait()
			#print('[resbf_flush]2 et set:',et.is_set(),'ee set:',ee.is_set())
			ee.wait()
			print('last resbf size ;',resbf.qsize())
			while not resbf.empty():
				errline+=1
				try:
					v=resbf.get_nowait()
				except:
					continue
				try:
					reslog.write(v)
				except:
					print('reslog write erroe at line:',errline,v)
					continue
			reslog.flush()
			return

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
		time.sleep(0.5)

def c_e_th():
	global procs
	thp=[]
	print('event tid',os.getpid(),'is starting...')
	print('res_save_tid',os.getpid(),'is starting...')
	pevent=threading.Thread(target=efunc,name='pevent_tid='+str(os.getpid()))
	pevent.start()
	for i in range(procs):
		res=threading.Thread(target=resbf_flush,name='res_save_tid='+str(os.getpid())+'/'+str(i))
		thp.append(res)
	for a in thp:
		a.start()
	for b in thp:
		b.join()
	print('[c_e_th]resbf is over......')
	pevent.join()
	#wbar=threading.Thread(target=wfunc_bar,name='wbar_tid='+str(os.getpid()))
	#wbar.start()
	print('\n[c_e_th]there is no more task so efunc done,efunc use time:%.2f' % (time.time()-st)+'s')
	print('='*60)
	print('[c_e_th]waiting for wfunc thread over...')
	print('[c_e_th]ee set:',ee.is_set())
	#wbar.join()

def c_w_th(ths):
	thp=[]
	for i in range(ths):
		t=threading.Thread(target=wfunc,name='tid'+str(os.getpid())+r'/'+str(i))
		thp.append(t)
	for a in thp:
		a.start()
	for b in thp:
		b.join(2)

def pefunc():
	print(os.getpid(),'pefunc is running...')
	c_e_th()
	print('[pefunc]pefunc done......')

def pwfunc():
	global allcount,alltime
	print('[pwfunc]pid =',os.getpid(),'is running...')
	c_w_th(ths)
	allcount.value+=pcount
	alltime.value+=ptime
	print('\n[pwfunc]pid='+str(os.getpid())+' real time: '+str(ptime)+'s\tcounts:'+str(pcount))
	print('[pwfunc]'+str(os.getpid())+' wfunc is done use time:%.2f' % (time.time()-st)+'s')
	#print('[pwfunc]ee set',ee.is_set())
	#print('[pwfunc]resbf qsize',resbf.qsize())

def delcache():
	cachedir='__pycache__'
	try:
		os.chdir(cachedir)
	except:
		return
	flist=os.listdir()
	while True:
		try:
			os.remove(flist.pop())
		except:
			os.rmdir('../'+cachedir)
			os.chdir('../')
			return

if __name__=='__main__':
	st=time.time()
#public var set
	procs=int(input('set procs:'))-1
	ths=int(input('set thread count:'))
	wqs=ths
	#procs=os.cpu_count()
	eq=Queue(procs)
	task=int(input('set task count:'))
	bartask=task
	alltime=Value('i',0)
	allcount=Value('i',0)
	bar=Value('i',1)

#log file set
	delcache()
	fname='./result.log'
	try:
		os.remove(fname)
	except:
		pass
	os.path.exists(fname)
	reslog=open(fname,'a')
	resbf=Queue()
	errline=0

#set var to event procs
	ee=Event()
	et=threading.Event()
	pe=Process(target=pefunc)
	pe.start()
	del et

#set var to work procs
	wq=queue.Queue(wqs)
	wcq=queue.Queue(1)
	we=threading.Event()
	weqget=True
	wg=None
	ptime=0
	pcount=0
	threadover=0
	test=0
	pw=Pool(procs)
	for i in range(procs):
		pw.apply_async(pwfunc)
	pw.close()
	pw.join()
	ee.set()
	print('main ee set',ee.is_set())
	pe.join()
	print('resbf size ;',resbf.qsize())
	reslog.close()

	print('\nreal time: '+str(alltime.value)+'s\tcounts: '+str(allcount.value))
	print('use time: %.2f' % (time.time()-st)+'s')