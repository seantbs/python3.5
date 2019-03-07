#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Event,JoinableQueue,Pool,Process,Value
import io,os,sys,time,random,threading,queue
import pgbar,tracemalloc

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

def workers_y(a):
	for i in range(a):
		yield work()

def efunc():
	global task,wqs,procs,taskend
	print('[efunc]event tid',threading.current_thread().name,'is starting...')
	while True:
		if task != 0:
			while not eq.full():
				if task == 0:
					break
				eg=eq_put_y(task,wqs,procs)
				eql=[]
				#print('[eq_put]task =',task)
				eql.append(task)
				task=next(eg)
				eql.append(task)
				#print('[eq_put]eql :',eql)
				eq.put(eql)
		elif task == 0:
			break
		ee.clear()
		ee.wait()
	#print('[efunc]task =',task,'et set',et.is_set(),'| ee set',ee.is_set())
	n=0
	while True:
		while not eq.full():
			n+=1
			if n <= procs:
				eq.put('done')
				print('[efunc]n =',n,'eq empty',eq.empty(),'ee set:',ee.is_set())
				if procs == 1:
					ee.clear()
					taskend.value=True
					print('[efunc]',threading.current_thread().name,'<1> ee set:',ee.is_set())
					return
			elif n > procs and eq.empty():
				ee.clear()
				taskend.value=True
				print('[efunc]',threading.current_thread().name,'<1> ee set:',ee.is_set())
				return
		ee.clear()
		ee.wait()
	return

def eq_get():
	global wq,wqs,wg,procs,weqget,task
	wqe=[]
	wqa=None
	wqb=None

	if weqget:
		ee.set()
		while eq.empty():
			if not weqget:
				wq_put()
				return
			elif eq.empty() and taskend.value == True:
				weqget=False
				break
	else:
		wq_put()
		return

	if not eq.empty() and weqget:
		while True:
			if weqget:
				try:
					wqe=eq.get_nowait()
				except:
					print('[eq_get]',threading.current_thread().name,'wqe get failed|eq empty :',eq.empty(),'| wcq empty :',wcq.empty(),'|weqget:',weqget,'ee set:',ee.is_set())
					if not weqget:
						wq_get()
						return
					else:
						ee.set()
						#time.sleep(0.1)
						continue
			break
		eq.task_done()
		print('<%.4f s>' % (time.time()-st),'| [eq_get]',threading.current_thread().name,'wqe=',wqe,'| eq empty :',eq.empty(),'| we set',we.is_set(),'| ee set:',ee.is_set(),'| wcq empty :',wcq.empty(),)
		if wqe != 'done' and wqe != []:
			wqa=wqe.pop()
			wqb=wqe.pop()
			wg=wq_put_y(wqa,wqb)
			ee.set()
			wq_put()
			return
		elif wqe == 'done':
			weqget=False

def wq_put():
	global wg,wg_ready
	x=None
	try:
		x=next(wg)
	except:
		if not wg_ready:
			eq_get()
	if x != None:
		wq.put(x)

async def work():
	global pcount,workers,task,count
	while True:
		std = ''
		text = ''
		x = None
		if not wq.empty():
			x = wq.get()
			pcount+=1
		elif weqget and wq.empty():
			wq_put()
		if x != None:
			await slow_work(std,text,x)
			if count%(workers) < workers/100:
				await res_save()
		elif x == None and not weqget:
			while len(res_cache):
				await res_save()
			return

async def slow_work(std,text,x):
	global count,res_cache,ptime,pcount,fname
	r = random.randint(2,6)
	ptime+=r
	for i in range(r):
		text+='a'
		await asyncio.sleep(1)
	std=str(x)+'\t'+text+'\n'
	#print('[slow_work]x = %s,r = %s,std = %s' % (x,r,std))
	res_cache.append(std)
	count+=1
	if count%500 == 0:
		pgbar.bar(task,count,50,st)
	elif count == task:
		pgbar.bar(task,count,50,st)
		print('\n\n[work]work queue is empty,write to %s'%fname)
	#sys.stdout.write('\rcount = '+str(count)+'\t|cw = '+str(cw))

async def res_save():
	global wths,res_cache
	v=''
	for i in range(wths):
		try:
			v+=res_cache.pop()
		except:
			continue
	try:
		reslog.write(v)
	except:
		errlist.append(v)
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
	return

def c_e_th():
	global wths,procs
	thp=[]
	pevent=threading.Thread(target=efunc,name='pevent_tid='+str(os.getpid())+'/0')
	pevent.start()
	pevent.join()
	print('\n[c_e_th]there is no more task,efunc done,use time:%.2f' % (time.time()-st)+'s')
	print('='*60)
	print('[c_e_th]waiting for resbf thread over...')
	#wbar=threading.Thread(target=wfunc_bar,name='wbar_tid='+str(os.getpid()))
	#wbar.start()
	#wbar.join()
	return

def pefunc():
	print(os.getpid(),'pefunc is starting......')
	c_e_th()
	print('[pefunc]pefunc done......')
	return

def pwfunc():
	global allcount,alltime
	print('[pwfunc]pid =',os.getpid(),'is running...')
	loop = asyncio.get_event_loop()
	fs=asyncio.gather(*coros)
	loop.run_until_complete(fs)
	loop.close()
	
	allcount.value+=pcount
	alltime.value+=ptime
	print('tracemalloc:',tracemalloc.get_traced_memory())
	print('\n[pwfunc]pid='+str(os.getpid())+' real time: '+str(ptime)+'s\tcounts:'+str(pcount))
	print('[pwfunc]'+str(os.getpid())+' wfunc is done use time:%.2f' % (time.time()-st)+'s')
	print('[pwfunc]wq empty :',wq.empty(),'|wq size :',wq.qsize(),'| errlist count :',len(errlist))
	while len(errlist):
		reslog.write('err:\t'+errlist.pop())
		reslog.flush()
	return os.getpid()

def cb_w_p_fin(test):
	global p_fin_c,procs
	p_fin_c.append(test)
	print('[cb_w_p_fin]',p_fin_c)
	if len(p_fin_c) == procs:
		pw.terminate()
	return

def prepare(workers):
	print('[prepare]pid-%s prepare %d workers...'%(os.getpid(),workers))
	count=0
	coros=[]
	workers_g=workers_y(workers)
	while True:
		try:
			x = next(workers_g)
		except:
			break
		coros.append(x)
		count+=1
		if count%100 == 0:
			pgbar.bar(workers,count,50,st)
		elif count==workers:
			pgbar.bar(workers,count,50,st)
	print('\n[prepare]pid-%s workers is ready'%os.getpid())
	return coros

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
	return

if __name__=='__main__':
	tracemalloc.start()
	st=time.time()
	delcache()
#public var set
	procs=int(input('set procs:'))-1
	if procs <= 1:
		procs=1
	workers=int(input('set workers:'))
	task=int(input('set task:'))
	wqs=workers
	bartask=task
	#procs=os.cpu_count()
	eq=JoinableQueue(procs)
	taskend=Value('b',False)
	alltime=Value('i',0)
	allcount=Value('i',0)
	bar=Value('i',1)
	
#set var to event procs
	ee=Event()
	pe=Process(target=pefunc)
	pe.start()
	del bartask
	
#log file set
	fname='./result.log'
	try:
		os.remove(fname)
	except:
		pass
	os.path.exists(fname)
	reslog=open(fname,'a')

#set var to work procs
	wq=queue.Queue(int(workers*procs))
	wcq=queue.Queue(1)
	we=threading.Event()
	weqget=True
	wg=None
	wg_ready=False
	ptime=0
	pcount=0
	wq_cache=[]
	res_cache=[]
	errlist=[]
	p_fin_c=[]
	
	coros = prepare(workers)
	
	pw=Pool(procs)
	for _ in range(procs):
		pw.apply_async(pwfunc,(coros,),callback=cb_w_p_fin)
	#del wq,wg,ptime,pcount,wq_cache,res_cache,errlist
	pw.close()
	pw.join()
	print('pw is over......')
	pe.join()
	reslog.close()
	
	print('\nprocs : %s\tthread : %s\tqueue maxsize : %s' % (procs,wths,wq.maxsize))
	print('real time: '+str(alltime.value)+'s\tcounts: '+str(allcount.value))
	print('use time: %.2f' % (time.time()-st)+'s')