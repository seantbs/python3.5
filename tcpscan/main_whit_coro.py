#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Event,JoinableQueue,Pool,Process,Value,Queue
import io,os,sys,time,random,threading,queue,asyncio
import pgbar,tracemalloc,ports_g,iprange_g

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
	global task,wqs,procs
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
				#print('[efunc]n =',n,'eq empty',eq.empty(),'ee set:',ee.is_set())
				if procs == 1:
					ee.clear()
					return
			elif n > procs and eq.empty():
				ee.clear()
				return
		ee.clear()
		ee.wait()
	return

def progress():
	global bartask,procs
	print('[progress]workers are running...')
	ee.wait()
	for _ in range(procs):
		print('[progress]worker pid :',state_pid.get())
	while True:
		time.sleep(0.1)
		pgbar.bar(bartask,progress_count.value,50,st)
		if task == allcount.value:
			pgbar.bar(bartask,allcount.value,50,st)
			break

async def eq_get():
	global wqs,wg,wg_ready,weqget
	wqe=[]
	wqa=None
	wqb=None
	if not eq.empty() and weqget:
		wqe=eq.get()
		eq.task_done()
		#print('[eq_get]pid-%s wqe=%s'%(os.getpid(),wqe))
		if wqe != 'done' and wqe != []:
			wqa=wqe.pop()
			wqb=wqe.pop()
			wg=wq_put_y(wqa,wqb)
			ipg=iprange_g.ip_iter(ipseed,ipcounts)
			portg=ports_g.prange(ps,pe)
			wg_ready=True
			ee.set()
		elif wqe == 'done':
			weqget=False
			ee.set()
		#print('[eq_get]pid-%s [%s,%s] | eq empty:%s | weqget=%s'%(os.getpid(),wqa,wqb,eq.empty(),weqget))

async def wq_put():
	global wg,wg_ready
	x=None
	try:
		x=next(wg)
	except:
		wg_ready=False
		if not wg_ready and weqget:
			await eq_get()
	if x != None:
		wq.put(x)

async def work():
	global pcount,workers,task
	while True:
		std = ''
		text = ''
		x = None
		if not wq.empty():
			x = wq.get()
			#print('[work]pid-%s x = %s pcount=%s' % (os.getpid(),x,pcount))
		elif weqget and wq.empty():
			await wq_put()
		if x != None:
			await scan_tcp(host,port)
		elif x == None and not weqget:
			while len(res_cache):
				await res_save()
			break
	return

async def slow_work(std,text,x):
	global res_cache,ptime,pcount,fname,workers,task
	r = random.randint(2,6)
	ptime+=r
	for i in range(r):
		text+='a'
		await asyncio.sleep(1)
	std=str(x)+'\t'+text+'\n'
	#print('[slow_work]pid-%s x = %s,r = %s,std:%s' % (os.getpid(),x,r,std))
	res_cache.append(std)
	pcount+=1
	progress_count.value+=1
	if pcount%workers == 0:
		await res_save()

async def scan_tcp(host,port):
	global st
	host=''
	port=None
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	#addrinfo=socket.getaddrinfo(host,port)
	#print(addrinfo[0][4])
	constat=s.connect_ex((host,port))
	c=os.strerror(constat)
	#print('host:%s,port:%s -> %s%(host,port,c))
	std='%s\t%s\t%s'%(host,port,c)
	res_cache.append(std)
	ptime+=(time.time()-st)
	pcount+=1
	progress_count.value+=1
	s.close()
	if pcount%workers == 0:
		await res_save()

async def res_save():
	global workers,res_cache
	v=''
	for i in range(workers):
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

def c_e_th():
	pevent=threading.Thread(target=efunc,name='pevent_tid='+str(os.getpid())+'/0')
	pgbar_th=threading.Thread(target=progress,name='progress_th')
	pevent.start()
	pgbar_th.start()
	pgbar_th.join()
	pevent.join()

	print('\n[c_e_th]there is no more task,efunc done,use time:%.2f' % (time.time()-st)+'s')
	print('='*60)
	print('[c_e_th]waiting for resbf thread over...')
	#wbar=threading.Thread(target=wfunc_bar,name='wbar_tid='+str(os.getpid()))
	#wbar.start()
	#wbar.join()
	return

def pefunc():
	print('[pefunc]pid',os.getpid(),'pefunc is starting......')
	c_e_th()
	print('[pefunc]pefunc done......')
	return

def pwfunc():
	global pcount,ptime
	#print('[pwfunc]pid-',os.getpid(),'is running...')
	state_pid.put(os.getpid())
	coros = prepare(workers)
	loop = asyncio.get_event_loop()
	fs=asyncio.gather(*coros)
	loop.run_until_complete(fs)
	loop.close()
	alltime.value+=ptime
	allcount.value+=pcount
	ee.clear()
	ee.wait()
	print('\ntracemalloc:',tracemalloc.get_traced_memory())
	print('[pwfunc]pid='+str(os.getpid())+' real time: '+str(ptime)+'s\tcounts:'+str(pcount))
	print('[pwfunc]pid='+str(os.getpid())+' wfunc is done use time:%.2f' % (time.time()-st)+'s'+'\n[pwfunc]pid='+str(os.getpid())+' wq empty :',wq.empty(),'| errlist count :',len(errlist))
	while len(errlist):
		reslog.write('err:\t'+errlist.pop())
		reslog.flush()
	return os.getpid()

def cb_w_p_fin(test):
	global p_fin_c,procs
	p_fin_c.append(test)
	#print('[cb_w_p_fin]',p_fin_c)
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
	print('[prepare]pid-%s workers is ready'%os.getpid())
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
	parser=argparse.ArgumentParser(description='set host or ip range what will be scaned,input port range with int.default scan ports 1-1024.')
	parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
	parser.add_argument('-host',type=str,nargs='*',default='127.0.0.1',help="set host list like '192.168.0.1 192.168.0.2' default 127.0.0.1")
	parser.add_argument('-range',type=str,help="set ip range to scan like '192.168.0.1-192.168.1.1' just once")
	parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
	parser.add_argument('-ps',type=int,nargs='?',default=1,help='set start port vaule')
	parser.add_argument('-pe',type=int,nargs='?',default=1024,help='set end port vaule')
	parser.add_argument('-sp',type=int,nargs='+',help="set specify port vaule like '80 135 137'")
	parser.add_argument('-procs',type=int,nargs='?',default=1,help='set multiprocessing to running')
	parser.add_argument('-workers',type=int,nargs='?',default=1,help='set workers to running')
	parser.parse_args()
	args=parser.parse_args()

	ps=args.ps
	pe=args.pe
	sp=args.sp
	host=args.host
	ipr=args.range
	procs=args.procs
	workers=args.workers
	
	if type(proc) != int and proc > (os.cpu_count()*16):
		print('please set right procs number here and not greater than %s.'%(os.cpu_count()*16))
		sys.exit()
	elif type(workers) != int and workers > (65536/(os.cpu_count()*16)):
		print('please set right workers number here and not greater than %s.'%(65536/(os.cpu_count()*16)))
		sys.exit()

	ip=iprange_g.ip_check(ipr)
	port=ports_g.check_p(ps,pe)
	portlist=ports_g.check_p(sp)
	if ip and port:
		print("ip range :",ip)
		ipseed=iprange_g.set_seed(ip)
		ipcounts=iprange_g.ip_counts(ipseed)
		bartask=task=ipcounts
		print("the ip range start ",ips[0]," counts ",counts)
	elif ip and portlist:
		print("ip range :",ip)
		ipseed=iprange_g.set_seed(ip)
		ipcounts=iprange_g.ip_counts(ipseed)
		bartask=task=ipcounts
	elif host and port:
		print("ip range :",host)
		bartask=task=len(host)
	elif host and portlist:
		print("ip range :",host)
		bartask=task=len(host)
	else:
		print("please set ipaddr/port numbers or range")
		sys.exit(0)
	
	tracemalloc.start()
	st=time.time()
	delcache()

#public var set
	wqs=workers
	#procs=os.cpu_count()
	eq=JoinableQueue(procs)
	state_pid=Queue()
	alltime=Value('i',0)
	allcount=Value('i',0)
	progress_count=Value('i',0)
	
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
	weqget=True
	wg=None
	ipg=None
	scan=None
	wg_ready=False
	ptime=0
	pcount=0
	wq_cache=[]
	res_cache=[]
	errlist=[]
	p_fin_c=[]
	
#start procs
	ee=Event()
	pe=Process(target=pefunc)
	pe.start()
	
	pw=Pool(procs)
	for _ in range(procs):
		pw.apply_async(pwfunc,callback=cb_w_p_fin)
	pw.close()
	pe.join()
	ee.set()
	pw.join()
	print('\n[main]all works done,saved to %s'%fname)
	reslog.close()
	print('\nResult of Execution :')
	print('\nprocs : %s\tthread : %s\tqueue maxsize : %s' % (procs,workers,wq.maxsize))
	print('real time: '+str(alltime.value)+'s\tcounts: '+str(allcount.value))
	print('use time: %.4f' % (time.time()-st)+'s')