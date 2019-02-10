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
				et.set()
		elif task == 0:
			break
		ee.clear()
		ee.wait()
		et.set()
	#print('[efunc]task =',task,'et set',et.is_set(),'| ee set',ee.is_set())
	n=0
	while True:	
		if not eq.full():
			n+=1
			if n <= procs:
				eq.put('done')
				print('[efunc]n =',n,'eq empty',eq.empty(),'ee set:',ee.is_set())
			elif n > procs:
				ee.clear()
				et.set()
				taskend=True
				print('[efunc]',threading.current_thread().name,'<1> et set:',et.is_set(),'| ee set:',ee.is_set())
				return
		ee.clear()
		ee.wait()
 
def eq_get():
	global wqs,wg,procs,weqget,task
	wqe=[]
	wqa=None
	wqb=None
	#print(threading.current_thread().name,'weqget =',weqget,'ee set',ee.is_set())
	if weqget:
		ee.set()
		while eq.empty():
			print('[eq_get]',threading.current_thread().name,'wcq empty :',wcq.empty(),'weqget is',weqget,'| we set',we.is_set(),'| eq qsize:',eq.qsize())
			if not weqget or not ee.is_set():
				break
	else:
		wfunc()
		return

	if not eq.empty() and weqget:
		while True:
			try:
				wqe=eq.get_nowait()
			except:
				print('[eq_get]',threading.current_thread().name,'wqe get failed|eq empty :',eq.empty(),'| wcq empty :',wcq.empty(),'|weqget:',weqget)
				if not weqget:
					wfunc()
					return
				else:
					ee.set()
					continue
			break
		print('<%.4f s>' % (time.time()-st),'| [eq_get]',threading.current_thread().name,'wqe=',wqe,'| eq empty :',eq.empty(),'| we set',we.is_set(),'| ee set:',ee.is_set(),'| wcq empty :',wcq.empty(),)
		if wqe != 'done' and wqe != []:
			wqa=wqe.pop()
			wqb=wqe.pop()
			wg=wq_put_y(wqa,wqb)
			ee.set()
			wq_put()
		elif wqe == 'done':
			weqget=False
			ee.set()
	#print('[eq_get]',threading.current_thread().name,'return to wfunc','we set :',we.is_set(),'ee set :',ee.is_set(),'| eq empty :',eq.empty(),'wcq empty :',wcq.empty(),'weqget :',weqget)
	we.set()
	wfunc()

def wq_put():
	global wg,weqget
	x=None
	if not we.is_set() and not wcq.empty():
		we.set()
	if weqget:
		try:
			x=next(wg)
		except:
			if not wcq.empty():
				wcq.get_nowait()
				we.clear()
			print('[wq_put]',threading.current_thread().name,'return to wfunc','wcq empty :',wcq.empty(),'| eq empty :',eq.empty(),'weqget =',weqget,'we set',we.is_set())
			wfunc()
			return
	else:
		print('[wq_put]',threading.current_thread().name,'return to wfunc','wcq empty :',wcq.empty(),'| eq empty :',eq.empty(),'weqget =',weqget,'we set',we.is_set())
		wfunc()
		return
	#print('[wq_put]',threading.current_thread().name,'x =',x,'we set',we.is_set())
	if not wq.full() and x != None:
		try:
			wq.put_nowait(x)
		except:
			pass
	#print('[wq_put]check 2 :',threading.current_thread().name)
	wfunc()

def wfunc():
	global ptime,pcount,resbf,threadover,weqget,errlist,th_fin_c
	x=None
	n=0
	while not wq.empty():
		try:
			x=wq.get_nowait()
		except:
			break
		text=''
		#print('[wfunc]',threading.current_thread().name,'x =',x)
		r=random.randint(2,6)
		for i in range(r):
			text+='a'
			time.sleep(1)
		std=str(x)+'\t'+text+'\n'
		try:
			resbf.put_nowait(std)
		except:
			errlist.append(std)
		#print('[wfunc]',threading.current_thread().name,'std :',std)
		wq.task_done()
		ptime+=r
		pcount+=1
		n+=1

	if wcq.empty():
		try:
			wcq.put_nowait(threading.current_thread().name)
		except:
			wfunc()
			return
		print('[wfunc]return to eq_get()',threading.current_thread().name,'wcq empty',wcq.empty(),'we set',we.is_set(),'weqget =',weqget)
		we.clear()
		eq_get()
		return
	elif not weqget and not wcq.empty():
		#print('[wfunc]check 3 alive thresds :',threading.current_thread().name,threading.current_thread().is_alive())
		if ee.is_set():
			ee.clear()
		return
	we.wait()
	#print('[wfunc]check 1 :',threading.current_thread().name)
	wq_put()

def resbf_flush(ps):
	global resbf,reslog,errline,task,taskend
	print('[resbf_flush]res_save_tid',threading.current_thread().name,'is starting...')
	while True:
		resbfqs=resbf.qsize()
		#print('[resbf_flus]task!=0,resbf qsize =',resbfqs)
		if resbfqs >= ps:
			thqs=int((resbfqs-resbfqs%ps)/ps)
		else:
			thqs=resbfqs
		#print('[resbf_flus]',threading.current_thread().name,'task!=0,thqs =',thqs)
		for i in range(thqs):
			try:
				v=resbf.get_nowait()
			except:
				continue
			#print('[resbf_flus]v =',v)
			try:
				reslog.write(v)
			except:
				errline+=1
				print('reslog write erroe at line:',errline,v)
		reslog.flush()
		#print('[resbf_flush]et set:',et.is_set(),'taskend =',taskend)
		if taskend == False:
			et.clear()
			et.wait()
		elif taskend == True:
			et.wait()
			#print('[resbf_flush]',threading.current_thread().name,'<2> et set:',et.is_set(),'| end set:',end.is_set())
			end.wait()
			#print('[resbf_flush]',threading.current_thread().name,'<3> et set:',et.is_set(),'| end set:',end.is_set())
			#print('[resbf_flush]',threading.current_thread().name,'last resbf size ;',resbf.qsize())
			while not resbf.empty():
				try:
					v=resbf.get_nowait()
				except:
					continue
				#print('[resbf_flush]',threading.current_thread().name,'check point.....','et set:',et.is_set(),'| resbf empty :',resbf.empty(),'v=',v)
				try:
					reslog.write(v)
				except:
					errline+=1
					print('reslog write erroe at line:',errline,v)
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
	global wths,procs
	thp=[]
	pevent=threading.Thread(target=efunc,name='pevent_tid='+str(os.getpid())+'/0')
	pevent.start()
	x=int(wths/1000)
	if wths/1000 <= 1:
		ths=procs
	else:
		ths=procs*x
	for i in range(ths):
		rbf=threading.Thread(target=resbf_flush,args=(ths,),name='res_save_tid='+str(os.getpid())+'/'+str(i+1))
		thp.append(rbf)
	for a in thp:
		a.start()
	pevent.join()
	print('\n[c_e_th]there is no more task,efunc done,use time:%.2f' % (time.time()-st)+'s')
	print('='*60)
	print('[c_e_th]waiting for resbf thread over...')
	for b in thp:
		b.join()
	print('[c_e_th]errline =',errline)
	print('[c_e_th]resbf is over......')

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
	print(os.getpid(),'pefunc is starting......')
	c_e_th()
	print('[pefunc]pefunc done......')

def pwfunc():
	global allcount,alltime
	print('[pwfunc]pid =',os.getpid(),'is running...')
	c_w_th(wths)
	allcount.value+=pcount
	alltime.value+=ptime
	print('\n[pwfunc]pid='+str(os.getpid())+' real time: '+str(ptime)+'s\tcounts:'+str(pcount))
	print('[pwfunc]'+str(os.getpid())+' wfunc is done use time:%.2f' % (time.time()-st)+'s')
	print('[pwfunc]wq empty :',wq.empty(),'|wq size :',wq.qsize(),'| errlist count :',len(errlist))
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
def cb_test(test):
	global p_fin_c,procs
	p_fin_c.append(test)
	print('[cb_test]',p_fin_c)
	if len(p_fin_c) == procs:
		pw.terminate()

if __name__=='__main__':
	st=time.time()
#public var set
	procs=int(input('set procs:'))-1
	if procs <= 1:
		procs=1
	wths=int(input('set thread count:'))
	wqs=wths
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
	end=Event()
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
	errlist=[]
	p_fin_c=[]
	pw=Pool(procs)
	for i in range(procs):
		pw.apply_async(pwfunc,callback=cb_test)
	pw.close()
	pw.join()
	print('pw is over......')
	end.set()
	print('mainend end set :',end.is_set())
	pe.join()
	print('unfinished resbf size ;',resbf.qsize())
	reslog.close()

	print('\nreal time: '+str(alltime.value)+'s\tcounts: '+str(allcount.value))
	print('use time: %.2f' % (time.time()-st)+'s')