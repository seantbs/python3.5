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
	x=None
	#print(threading.current_thread().name,'weqget =',weqget,'ee set',ee.is_set())
	while True:
		try:
			x=next(wg)
		except:
			break
		#print('[eq_get]',threading.current_thread().name,'wcq empty:',wcq.empty(),'we set:',we.is_set(),'x=',x)
		if not wq.full() and x != None:
			try:
				wq.put_nowait(x)
			except:
				pass
		if not we.is_set() and not wcq.empty():
			we.set()

	if weqget:
		ee.set()
		while eq.empty():
			print('[eq_get]',threading.current_thread().name,'wcq empty :',wcq.empty(),'weqget is',weqget,'| ee set:',ee.is_set(),'| we set',we.is_set(),'| eq qsize:',eq.qsize())
			if not weqget:
				we.set()
				wq_put()
				return
			elif eq.empty() and taskend.value == True:
				weqget=False
				we.set()
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
			we.set()
			wq_put()
			return
		elif wqe == 'done':
			weqget=False
	#print('[eq_get]',threading.current_thread().name,'return to wfunc','we set :',we.is_set(),'ee set :',ee.is_set(),'| eq empty :',eq.empty(),'wcq empty :',wcq.empty(),'weqget :',weqget)
	we.set()
	wq_put()
	return

def wq_put():
	global wg,weqget,wq,wq_cache
	while True:
		x=None
		while len(wq_cache):
			#print('[wq_put]wq_cache len:',len(wq_cache))
			try:
				x=wq_cache.pop()
			except:
				continue
			if not wq.full() and x != None:
				try:
					wq.put(x)
				except:
					wq_cache.append(x)
			elif wq.full() and x != None:
				wq_cache.append(x)
				wq_get()
				return

		if weqget:
			try:
				x=next(wg)
			except:
				if not wcq.empty() and wq.empty():
					try:
						y=wcq.get()
					except:
						wq_get()
						return
					we.clear()
					print('[wq_put]return to wfunc()',threading.current_thread().name,'wcq empty',wcq.empty(),'we set',we.is_set(),'weqget =',weqget)
					wfunc()
					return
				#print('[wq_put]return to wq_get()',threading.current_thread().name,'wcq empty',wcq.empty(),'we set',we.is_set(),'weqget =',weqget)
				wq_get()
				return
			#print('[wq_put]',threading.current_thread().name,'wq full:',wq.full(),'|x=',x)
			if not wq.full() and x != None:
				try:
					wq.put_nowait(x)
				except:
					wq_cache.append(x)
			elif wq.full() and x != None:
				wq_cache.append(x)
				wq_get()
				return
		elif not weqget and not wq.empty():
			#print('[wq_put]',threading.current_thread().name,'return to wfunc 2 ','wcq empty :',wcq.empty(),'| eq empty :',eq.empty(),'weqget =',weqget,'we set',we.is_set())
			wq_get()
			return
		elif not weqget and wq.empty():
			wfunc()
			return

def wq_get():
	global ptime,pcount,resbf,weqget,errlist
	while not wq.empty():
		x=None
		std=''
		text=''
		try:
			x=wq.get_nowait()
		except:
			if wcq.empty():
				break
			else:
				time.sleep(0.1)
				continue
		print('[wq_get]',threading.current_thread().name,'x =',x)
		r=random.randint(2,6)
		for i in range(r):
			text+='a'
			time.sleep(1)
		std=str(x)+'\t'+text+'\n'
		#print('[wfunc]',threading.current_thread().name,'std :',std)
		res_cache.append(std)
		wq.task_done()
		ptime+=r
		pcount+=1
		if pcount%(wths) < wths/100:
			res_save()
	we.wait()
	wq_put()
	return

def wfunc():
	global resbf,weqget,errlist,wcq
	if wcq.empty():
		try:
			wcq.put_nowait(threading.current_thread().name)
		except:
			wq_get()
			return
		we.clear()
		#print(threading.current_thread().name,'wcq.queue.index:',wcq.queue.index(threading.current_thread().name),'wcq empty',wcq.empty())
		if wcq.queue.index(threading.current_thread().name) == 0:
			print('[wfunc]return to eq_get()',threading.current_thread().name,'wcq empty',wcq.empty(),'we set',we.is_set(),'weqget =',weqget)
			eq_get()
			return
		else:
			print('[wfunc]return to wq_get()',threading.current_thread().name,'wcq empty',wcq.empty(),'we set',we.is_set(),'weqget =',weqget)
			wq_get()
			return
	elif not weqget and not wcq.empty():
		if ee.is_set():
			ee.clear()
		elif not we.is_set():
			we.set()
		while len(res_cache):
			res_save()
		while len(errlist):
			v=''
			try:
				v+=res_cache.pop()
			except:
				continue
			reslog.write(v)
		return
	#print('[wfunc]',threading.current_thread().name,'return to wq_put wcq empty:',wcq.empty(),'| wq empty :',wq.empty(),'weqget =',weqget,'we set',we.is_set())
	we.wait()
	wq_get()
	return

def res_save():
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
	return

def pefunc():
	print(os.getpid(),'pefunc is starting......')
	c_e_th()
	print('[pefunc]pefunc done......')
	return

def pwfunc():
	global allcount,alltime
	print('[pwfunc]pid =',os.getpid(),'is running...')
	c_w_th(wths)
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

def cb_w_p_fin(test):
	global p_fin_c,procs
	p_fin_c.append(test)
	print('[cb_w_p_fin]',p_fin_c)
	if len(p_fin_c) == procs:
		pw.terminate()
	return
	
if __name__=='__main__':
	tracemalloc.start()
	st=time.time()
	delcache()
#public var set
	procs=int(input('set procs:'))
	wths=int(input('set thread count:'))
	task=int(input('set task count:'))
	wqs=wths
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
	wq=queue.Queue(int(wths*procs))
	wcq=queue.Queue(1)
	we=threading.Event()
	weqget=True
	wg=None
	ptime=0
	pcount=0
	wq_cache=[]
	res_cache=[]
	errlist=[]
	p_fin_c=[]
	pw=Pool(procs)
	for _ in range(procs):
		pw.apply_async(pwfunc,callback=cb_w_p_fin)
	#del wq,wg,ptime,pcount,wq_cache,res_cache,errlist
	pw.close()
	pw.join()
	print('pw is over......')
	pe.join()
	reslog.close()
	
	print('\nprocs : %s\tthread : %s\tqueue maxsize : %s' % (procs,wths,wq.maxsize))
	print('real time: '+str(alltime.value)+'s\tcounts: '+str(allcount.value))
	print('use time: %.2f' % (time.time()-st)+'s')