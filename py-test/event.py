#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

from multiprocessing import Event,Queue,Pool,Process,Value
import io,os,sys,time,random,threading,queue,pgbar

def eq_put_y(a,b,c):
	if a == 0:
		yield 0
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

def efunc():
	global task,wqs,procs,taskend
	print('[efunc]event tid',os.getpid(),'is running...')
	while True:
		if task != 0:
			while not eq.full():
				if task != 0:
					eg=eq_put_y(task,wqs,procs)
					eql=[]
					#print('[eq_put]task =',task)
					eql.append(task)
					task=next(eg)
					eql.append(task)
					#print('[eq_put]eql :',eql)
					eq.put(eql)
				else:
					break
		elif task == 0:
			break
		ee.clear()
		ee.wait()
		et.set()
	print('[efunc]task =',task,'et set',et.is_set(),'| ee set',ee.is_set())
	n=0
	while True:	
		while not eq.full():
			n+=1
			if n <= procs:
				eq.put(None)
				print('[efunc]n =',n,'eq empty',eq.empty(),'ee set:',ee.is_set())
			elif n > procs:
				print('[efunc]',threading.current_thread().name,'<1> et set:',et.is_set(),'| ee set:',ee.is_set())
				et.set()
				ee.clear()
				taskend=True
				return
		ee.clear()
		ee.wait()
 
def eq_get():
	global wqs,wg,procs,weqget
	wqe=[]
	wqa=None
	wqb=None
	#print(threading.current_thread().name,'weqget =',weqget,'ee set',ee.is_set())
	if eq.empty() and weqget:
		print('[eq_get]',threading.current_thread().name,'weqget is',weqget,'| we set',we.is_set(),'| ee set',ee.is_set())
		we.set()
	elif not eq.empty() and weqget:
		wqe=eq.get()
		print('[eq_get]',threading.current_thread().name,'wqe=',wqe,'| eq empty :',eq.empty(),'| we set',we.is_set(),'| ee set:',ee.is_set())
		if wqe != None:
			#print('[eq_get]wqe =',wqe)
			wqa=wqe.pop()
			wqb=wqe.pop()
			wg=wq_put_y(wqa,wqb)
			if eq.empty():
				ee.set()
			we.set()
			wq_put()
			return
		elif wqe == None:
			weqget=False
			ee.set()
			print('[eq_get]eq empty :',eq.empty(),threading.current_thread().name,'weqget is',weqget)
			we.set()
	print('[eq_get]',threading.current_thread().name,'return to wfunc','we set :',we.is_set(),'ee set :',ee.is_set(),'| eq empty :',eq.empty(),'wcq empty :',wcq.empty(),'weqget :',weqget)
	wfunc()

def wq_put():
	global wg,weqget
	x=None
	try:
		x=next(wg)
	except:
		if weqget:
			if not wcq.empty():
				wcq.get()
		we.clear()
		print('[wq_put]return to wfunc','wcq empty :',wcq.empty(),'we set',we.is_set())
		wfunc()
		return
	#print('[wq_put]',threading.current_thread().name,'x =',x,'we set',we.is_set())
	if not wq.full() and x != None:
		wq.put(x)
	wfunc()

def wfunc():
	global ptime,pcount,resbf,threadover,weqget
	x=None
	n=0
	while not wq.empty():
		text=''
		x=wq.get()
		r=random.randint(2,6)
		for i in range(r):
			text+='a'
			time.sleep(1)
		std=str(x)+'\t'+text+'\n'
		#print('[wfunc]',threading.current_thread().name,'std :',std,'thstatus :',threading.current_thread().isAlive())
		resbf.put_nowait(std)
		wq.task_done()
		ptime+=r
		pcount+=1
		n+=1

	if wcq.empty() and weqget:
		try:
			wcq.put_nowait(threading.current_thread().name)
		except:
			wq_put()
		#print('[wfunc]',threading.current_thread().name,'wcq empty',wcq.empty(),'we set',we.is_set())
		we.clear()
		eq_get()
	elif not weqget and not wcq.empty():
		#we.clear()
		#we.wait()
		we.set()
		#print('[wfunc]',threading.current_thread().name,threading.current_thread()._tstate_lock)
		return
	#print('[wfunc]',threading.current_thread().name,'wq is empty we set',we.is_set())
	we.wait()
	wq_put()

def resbf_flush(ps):
	global resbf,reslog,errline,task,taskend
	et.clear()
	while True:
		et.wait()
		resbfqs=resbf.qsize()
		#print('[resbf_flus]task!=0,resbf qsize =',resbfqs)
		if resbfqs >= ps:
			thqs=int((resbfqs-resbfqs%ps)/ps)
		else:
			thqs=resbfqs
		#print('[resbf_flus]',threading.current_thread().name,'task!=0,thqs =',thqs)
		for i in range(thqs):
			errline+=1
			try:
				v=resbf.get()
			except:
				break
			try:
				reslog.write(v)
			except:
				print('reslog write erroe at line:',errline,v)
				continue
		reslog.flush()
		print('[resbf_flush]et set:',et.is_set(),'taskend =',taskend)
		if taskend == False:
			et.clear()
		elif taskend == True:
			et.wait()
			print('[resbf_flush]',threading.current_thread().name,'<2> et set:',et.is_set(),'| ee set:',ee.is_set())
			ee.wait()
			print('[resbf_flush]',threading.current_thread().name,'<3> et set:',et.is_set(),'| ee set:',ee.is_set())
			#print('last resbf size ;',resbf.qsize())
			while not resbf.empty():
				errline+=1
				try:
					v=resbf.get()
				except:
					break
				try:
					reslog.write(v)
				except:
					print('reslog write erroe at line:',errline,v)
					continue
			reslog.flush()
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
		time.sleep(0.5)

def c_e_th():
	global ths,procs
	thp=[]
	print('event tid',os.getpid(),'is starting...')
	print('res_save_tid',os.getpid(),'is starting...')
	pevent=threading.Thread(target=efunc,name='pevent_tid='+str(os.getpid()))
	pevent.start()
	for i in range(procs*2):
		rbf=threading.Thread(target=resbf_flush,args=(procs*2,),name='res_save_tid='+str(os.getpid())+'/'+str(i))
		thp.append(rbf)
	for a in thp:
		a.start()
	pevent.join()
	print('\n[c_e_th]there is no more task,efunc done,use time:%.2f' % (time.time()-st)+'s')
	print('='*60)
	print('[c_e_th]waiting for resbf thread over...')
	print('[c_e_th]ee set:',ee.is_set())
	for b in thp:
		b.join()
	print('[c_e_th]resbf is over......')
	print('[c_w_th]thread set :',threading.current_thread().isAlive())
	#wbar=threading.Thread(target=wfunc_bar,name='wbar_tid='+str(os.getpid()))
	#wbar.start()
	#wbar.join()

def c_w_th(ths):
	thp=[]
	for i in range(ths):
		t=threading.Thread(target=wfunc,name='tid'+str(os.getpid())+r'/'+str(i))
		thp.append(t)
	for a in thp:
		a.start()
	for b in thp:
		b.join()
	print('\n[c_w_th]',os.getpid(),'wq unfinished tasks :',wq.unfinished_tasks)
	print('[c_w_th]ee set',ee.is_set(),'| resbf qsize:',resbf.qsize())
	
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
	print('[pwfunc]wq empty :',wq.empty(),'|wq size :',wq.qsize())
	print('[c_w_th]thread set :',threading.current_thread().activeCount())
	
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
	taskend=False
	pe=Process(target=pefunc)
	pe.start()
	del et,taskend,bartask

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
	print('main ee set :',ee.is_set())
	pe.join()
	print('unfinished resbf size ;',resbf.qsize())
	reslog.close()

	print('\nreal time: '+str(alltime.value)+'s\tcounts: '+str(allcount.value))
	print('use time: %.2f' % (time.time()-st)+'s')