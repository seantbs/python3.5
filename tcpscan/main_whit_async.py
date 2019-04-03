#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Event,JoinableQueue,Pool,Process,Value,Queue
import io,os,sys,time,threading,queue,asyncio,socket,argparse
import pgbar,tracemalloc,ports_g,iprange_g

def eq_put_y(task,workers,procs):
	if task == 0:
		yield 0
	if procs == 1:
		for i in range(procs):
			if task >= workers:
				task-=workers
				yield task
			else:
				yield 0
	elif procs > 1:
		for i in range(procs):
			if task >= workers*procs:
				task-=workers
				yield task
			elif task*procs >= workers/procs and task < workers*procs:
				if task > procs:
					task=task-(int(task/procs)+task%procs)
					yield task
				elif task < procs:
					yield 0
			elif task*procs < workers/procs:
					yield 0

def eq_put_iprange(task,workers,procs,ipseed,wqport):
	while True:
		if task != 0:
			while not eq.full():
				if task == 0:
					break
				eg=eq_put_y(task,workers,procs)
				eql=[]
				#print('[eq_put_iprange]task =',task)
				a=task;task=next(eg);c=a-task
				#print('[eq_put_iprange]ipseed:',ipseed)
				eql.append(ipseed)
				ipseed=iprange_g.set_end(ipseed,c)
				eql.append(c)
				eql.append(wqport)
				print('[eq_put_iprange]eql :',eql,'task=',task)
				eq.put(eql)
		elif task == 0:
			break
		ee.clear()
		ee.wait()

def eq_put_iprange_fast(task,ipseed,port_g):
	portlist=[]
	iplist=[]
	n=0
	ipg=iprange_g.ip_iter(ipseed,task)
	for ip in ipg:
		iplist.append(ip)
	for p in port_g:
		if n > workers:
			while True:
				if not eq.full():
					eql=eq_put_iprange_fast_set(ipseed,task,portlist)
					eq.put(eql)
					portlist=[]
					n=0
					break
				else:
					ee.clear()
					ee.wait()
		n+=1
		portlist.append(p)
	while True:
		if not eq.full() and len(portlist) != 0:
			eql=eq_put_iprange_fast_set(ipseed,task,portlist)
			eq.put(eql)	
		elif len(portlist) == 0:
			return
		else:
			ee.clear()
			ee.wait()

def eq_put_iplist(task,workers,procs,ipseed,wqport):
	while True:
		if task != 0:
			while not eq.full():
				if task == 0:
					break
				eg=eq_put_y(task,workers,procs)
				#print('[eq_put_iplist]task =',task)
				a=task;task=next(eg)
				for i in range(task,a):
					eql=[]
					eql.append(ipseed[i])
					eql.append('list')
					eql.append(wqport)
					print('[eq_put_iplist]eql :',eql,'task=',task)
					eq.put(eql)
		elif task == 0:
			break
		ee.clear()
		ee.wait()

def eq_put_fast_set(iplist,portlist):
	eql=[]
	eql.append(iplist)
	eql.append('fast')
	eql.append(portlist)
	print('[eq_put_iplist_fast]eql :',eql)
	return eql

def eq_put_iplist_fast(workers,ipseed,port_g):
	portlist=[]
	iplist=[]
	n=0
	for ip in ipseed:
		iplist.append(ip)
	for p in port_g:
		if n > workers:
			while True:
				if not eq.full():
					eql=eq_put_fast_set(iplist,portlist)
					eq.put(eql)
					portlist=[]
					n=0
					break
				else:
					ee.clear()
					ee.wait()
		n+=1
		portlist.append(p)
	while True:
		if not eq.full() and len(portlist) != 0:
			eql=eq_put_iplist_fast_set(ip,portlist)
			eq.put(eql)
			portlist=[]
			n=0
		elif len(portlist) == 0:
			continue
		else:
			ee.clear()
			ee.wait()

def get_ip_g(check_ip,host,ipr):
	if check_ip > 0:
		ipseed=iprange_g.set_seed(ipr)
		return ipseed
	elif check_ip == 0:
		ipseed=host
		return ipseed

def get_port_g(check_port,ps,pe,sp):
	if check_port > 0:
		port_g=ports_g.port_range(ps,pe)
		return port_g
	elif check_port == 0:
		port_g=ports_g.port_list(sp)
		return port_g

def efunc():
	global alltask,workers,procs,chekc_ip,check_port,ps,pe,sp,host,ipr
	print('[efunc]event tid',threading.current_thread().name,'is starting...')
	port_g=get_port_g(check_port,ps,pe,sp)
	ipseed_type=get_ip_g(check_ip,host,ipr)
	print('[efunc]port_g:',port_g,'|ipseed_type:',type(ipseed_type))
	if type(ipseed_type) == tuple:
		if alltask < procs:
			eq_put_iprange_fast(alltask,ipseed_type[0],port_g)
		else:
			while True:
				try:
					wqport=next(port_g)
					#print('[efunc]wqport:',wqport)
				except:
					break
				task=alltask
				eq_put_iprange(task,workers,procs,ipseed_type[0],wqport)
	elif type(ipseed_type) == list:
		if alltask < procs:
			eq_put_iplist_fast(workers,ipseed_type,port_g)
		else:
			while True:
				try:
					wqport=next(port_g)
					#print('[efunc]wqport:',wqport)
				except:
					break
				task=alltask
				eq_put_iplist(task,workers,procs,ipseed_type,wqport)
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
				return
		ee.clear()
		ee.wait()
	return

def progress():
	global alltask,procs,ports,st,progress_count,allcount
	bartask=alltask*ports
	print('[progress]workers are running...bartask:',bartask)
	ee.wait()
	for _ in range(procs):
		print('[progress]worker pid :',state_pid.get())
	while True:
		time.sleep(1)
		pgbar.bar(bartask,progress_count.value,50,st)
		print('[progress]progress_count=',progress_count.value,'allcount=',allcount.value)
		if bartask == allcount.value:
			pgbar.bar(bartask,allcount.value,50,st)
			break

def c_e_th():
	pevent=threading.Thread(target=efunc,name='pevent_tid='+str(os.getpid())+'/0')
	#pgbar_th=threading.Thread(target=progress,name='progress_th')
	pevent.start()
	#pgbar_th.start()
	#pgbar_th.join()
	pevent.join()
	print('\n[c_e_th]there is no more task,efunc done,use time:%.2f' % (time.time()-st)+'s')
	print('='*60)
	return

def pefunc():
	print('[pefunc]pid',os.getpid(),'pefunc is starting......')
	c_e_th()
	print('[pefunc]pefunc done......')
	return

###################################################################################
def eq_get():
	global wg,wg_ready,weqget,wqport,ip_g
	wqe=[]
	wqport=None
	ip_g=None
	if not eq.empty() and weqget:
		wqe=eq.get()
		print('[eq_get]pid',os.getpid(),'wqe=',wqe)
		eq.task_done()
		#print('[eq_get]pid-%s wqe=%s'%(os.getpid(),wqe))
		if wqe != 'done' and wqe != [] and wqe[-2] != 'fast':
			wqport=wqe.pop()
			ipcounts=wqe.pop()
			ipseed=wqe.pop()
			#print('[eq_get]wqe:',wqe)
			ip_g=iprange_g.ip_iter(ipseed,ipcounts)
			wg_ready=True
			ee.set()
			return
		elif wqe != 'done' and wqe != [] and wqe[-2] == 'fast':
			wqe.pop(-2)
			wqport=wqe.pop()
			#print('[eq_get]wqe:',wqe)
			ip_g=(x for x in wqe)
			wg_ready=True
			ee.set()
			return
		elif wqe == 'done':
			weqget=False
			ee.set()
			return
		#print('[eq_get]pid-%s [%s,%s] | eq empty:%s | weqget=%s'%(os.getpid(),wqa,wqb,eq.empty(),weqget))
	elif eq.empty() and weqget:
		ee.set()
		eq_get()
	elif eq.empty() and not weqget:
		return

def wq_put():
	global wg_ready,wqport,ip_g,weqget
	x=None
	if weqget:
		try:
			x=next(ip_g)
			#print('[wq_put]pid',os.getpid(),'x=',x)
		except:
			#print('[wq_put]pid',os.getpid(),'x=None,ip_g is stop|wg_ready:',wg_ready)
			wg_ready=False
			if not wg_ready and weqget:
				eq_get()
			elif not weqget:
				return
	else:
		return
	if x != None:
		x=(x,wqport)
		#print('[wq_put]x=',x)
		wq.put(x)
		return

async def work(loop):
	global opencount,closecount,ptime,progress_count
	while True:
		addr=None
		con=''
		wst=time.time()
		if not wq.empty():
			addr = wq.get()
			#print('[work]pid',os.getpid(),'get addr:',addr)
			s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setblocking(0)
			progress_count.value+=1
			try:
				con=await loop.sock_connect(s,addr)
			except OSError as err:
				closecount+=1
				err=str(err)
				std='%s,%s,%s\n'%(addr[0],addr[1],err)
				res_cache.append(std)
				#print('[work]pid',os.getpid(),addr,err)
			if con == None:
				opencount+=1
				#print('pid',os.getpid(),addr,'open')
				std='%s,%s,open\n'%(addr[0],addr[1])
				res_cache.append(std)
			s.close()
			ptime+=time.time()-wst
		elif weqget and wq.empty():
			wq_put()
		elif addr == None and not weqget:
			#print('[work]pid',os.getpid(),'progress_count.value',progress_count.value)
			break
	return

def res_thread(workers,res_cache):
	global weqget,work_done
	print('[res_thread]res_thread tid',threading.current_thread().name,'is starting...')
	while True:
		#print('[res_thread]pid',os.getpid(),'weqget:',weqget)
		if not work_done:
			res_save(workers,res_cache)
		elif work_done:
			while len(res_cache):
				res_save(workers,res_cache)
			break
		time.sleep(1)
	return

def res_save(workers,res_cache):
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

def pwfunc():
	global alltime,allcount,work_done
	#print('[pwfunc]pid-',os.getpid(),'is running...')
	state_pid.put(os.getpid())
	res_save_thread=threading.Thread(target=res_thread,args=(workers,res_cache),name='res_thread_tid='+str(os.getpid()))
	res_save_thread.start()
	selloop=asyncio.SelectorEventLoop()
	asyncio.set_event_loop(selloop)
	loop = asyncio.get_event_loop()
	corus = prepare(workers,loop)
	fs=asyncio.gather(*corus)
	loop.run_until_complete(fs)
	loop.close()
	work_done=True
	res_save_thread.join()
	alltime.value+=ptime
	#print('[pwfunc]pid',os.getpid(),'ee set:',ee.is_set())
	#print('\ntracemalloc:',tracemalloc.get_traced_memory())
	print('[pwfunc]pid=%s\treal time:%.4fs\topen_counts:%s\tclose_counts:%s' % (os.getpid(),ptime,opencount,closecount))
	print('[pwfunc]pid=%s\tuse time:%.4fs'%(os.getpid(),time.time()-st)+'\twq empty:'+str(wq.empty())+'\tres_err count:'+str(len(errlist)))
	
	while len(errlist):
		reslog.write('err:\t'+errlist.pop())
		reslog.flush()
	return os.getpid(),opencount,closecount

def cb_w_p_fin(result):
	global p_fin_c,procs,opencount,closecount
	opencount+=result[1]
	closecount+=result[2]
	p_fin_c.append(result[0])
	#print('[cb_w_p_fin]',p_fin_c)
	if len(p_fin_c) == procs:
		p_wfunc.terminate()
	return

def workers_y(a,loop):
	for i in range(a):
		yield work(loop)

def prepare(workers,loop):
	count=0
	corus=[]
	workers_g=workers_y(workers,loop)
	while True:
		try:
			x = next(workers_g)
		except:
			break
		corus.append(x)
		count+=1
	#print('[prepare]pid-%s workers is ready'%os.getpid())
	return corus
############################################################################
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

def check_input():
	parser=argparse.ArgumentParser(description='set host or ip range what will be scaned,input port range with int.default scan ports 1-1024.')
	parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
	parser.add_argument('-host',type=str,nargs='*',default='127.0.0.1',help="set host list like '192.168.0.1 192.168.0.2' default 127.0.0.1")
	parser.add_argument('-range',type=str,help="set ip range to scan like '192.168.0.1-192.168.1.1' just once")
	parser.add_argument('-ps',type=int,nargs='?',default=1,help='set start port vaule')
	parser.add_argument('-pe',type=int,nargs='?',default=1024,help='set end port vaule')
	parser.add_argument('-sp',type=int,nargs='+',help="set specify port vaule like '80 135 137'")
	parser.add_argument('-procs',type=int,nargs='?',default=os.cpu_count(),help='set multiprocessing to running')
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
	if type(procs) != int and procs > (os.cpu_count()*16):
		print('please set right procs number here and not greater than %s.'%(os.cpu_count()*16))
		sys.exit()
	elif type(workers) != int and workers > (65536/(os.cpu_count()*16)):
		print('please set right workers number here and not greater than %s.'%(65536/(os.cpu_count()*16)))
		sys.exit()

	ip=iprange_g.check_iprange(ipr)
	host=iprange_g.check_host(host)
	port=ports_g.check_p(ps,pe)
	portlist=ports_g.check_p(sp)
	
	if ip and portlist:
		print("ip range :",ip)
		ipseed=iprange_g.set_seed(ip)
		ipcounts=iprange_g.ip_counts(ipseed)
		print("the ip range start ",ipseed[0]," counts ",ipcounts)
		return ipcounts,len(sp),1,0,workers,procs,ps,pe,sp,host,ip
	elif host and portlist:
		print("ip range :",host)
		return len(host),len(sp),0,0,workers,procs,ps,pe,sp,host,ip
	elif ip and port:
		print("ip range :",ip)
		ipseed=iprange_g.set_seed(ip)
		ipcounts=iprange_g.ip_counts(ipseed)
		print("the ip range start ",ipseed[0]," counts ",ipcounts)
		return ipcounts,pe-ps+1,1,1,workers,procs,ps,pe,sp,host,ip
	elif host and port:
		print("ip range :",host)
		return len(host),pe-ps+1,0,1,workers,procs,ps,pe,sp,host,ip
	else:
		print("please set ipaddr/port numbers or range")
		sys.exit(0)

############################################################################################
if __name__=='__main__':
	alltask,ports,check_ip,check_port,workers,procs,ps,pe,sp,host,ipr=check_input()
	print('[mian]alltask:%s ports:%s check_ip:%s check_port:%s'%(alltask,ports,check_ip,check_port))
	#tracemalloc.start()
	st=time.time()
	delcache()

#public var set
	eq=JoinableQueue(procs)
	state_pid=Queue()
	alltime=Value('d',0.0)
	#allcount=Value('i',0)
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
	ip_g=None
	wqport=None
	wg_ready=False
	work_done=False
	ptime=0
	opencount=0
	closecount=0
	wq_cache=[]
	res_cache=[]
	errlist=[]
	p_fin_c=[]
	
#start procs
	ee=Event()
	p_efunc=Process(target=pefunc)
	p_efunc.start()
	
	p_wfunc=Pool(procs)
	for _ in range(procs):
		p_wfunc.apply_async(pwfunc,callback=cb_w_p_fin)
	p_wfunc.close()
	p_efunc.join()
	p_wfunc.join()
	print('\n[main]all works done,saved to %s'%fname)
	reslog.close()
	print('\nResult of Execution :')
	print('\nprocs : %s\tcorus : %s\tqueue maxsize : %s' % (procs,workers,wq.maxsize))
	print('real time:%.4fs\topened:%s\tclosed:%s\tall:%s'%(alltime.value,opencount,closecount,opencount+closecount))
	print('use time: %.4f' % (time.time()-st)+'s')