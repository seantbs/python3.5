#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Event,JoinableQueue,Pool,Process,Value,Queue
import io,os,sys,time,threading,queue,asyncio,socket,argparse
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

def eq_put_iprange(task,wqs,procs,ipseed,wqport):
	while True:
		if task != 0:
			while not eq.full():
				if task == 0:
					break
				eg=eq_put_y(task,wqs,procs)
				eql=[]
				print('[eq_put_iprange]task =',task)
				a=task;task=next(eg);c=a-task
				print('[eq_put_iprange]ipseed:',ipseed)
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

def eq_put_iplist(task,wqs,procs,ipseed,wqport):
	while True:
		if task != 0:
			while not eq.full():
				if task == 0:
					break
				eg=eq_put_y(task,wqs,procs)
				eql=[]
				print('[eq_put_iplist]task =',task)
				a=task;task=next(eg)
				for i in range(task,a):
					eql.append(ipseed[i])
				eql.append('list')
				eql.append(wqport)
				print('[eq_put_iplist]eql :',eql,'task=',task)
				eq.put(eql)
		elif task == 0:
			break
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
	global alltask,wqs,procs,chekc_ip,check_port,ps,pe,sp,host,ipr
	print('[efunc]event tid',threading.current_thread().name,'is starting...')
	port_g=get_port_g(check_port,ps,pe,sp)
	ipseed_type=get_ip_g(check_ip,host,ipr)
	print('[efunc]port_g:',port_g,'|ipseed_type:',type(ipseed_type))
	if type(ipseed_type) == tuple:
		while True:
			try:
				wqport=next(port_g)
				#print('[efunc]wqport:',wqport)
			except:
				break
			task=alltask
			eq_put_iprange(task,wqs,procs,ipseed_type[0],wqport)
	elif type(ipseed_type) == list:
		while True:
			try:
				wqport=next(port_g)
				#print('[efunc]wqport:',wqport)
			except:
				break
			task=alltask
			eq_put_iplist(task,wqs,procs,ipseed_type,wqport)
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
	global alltask,procs,ports,st
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
	print('[c_e_th]waiting for resbf thread over...')
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
		if wqe != 'done' and wqe != [] and wqe[-2] != 'list':
			wqport=wqe.pop()
			ipcounts=wqe.pop()
			ipseed=wqe.pop()
			#print('[eq_get]wqe:',wqe)
			ip_g=iprange_g.ip_iter(ipseed,ipcounts)
			wg_ready=True
			ee.set()
			return
		elif wqe != 'done' and wqe != [] and wqe[-2] == 'list':
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
		#print('[eq_get]pid-%s [%s,%s] | eq empty:%s | weqget=%s'%(os.getpid(),wqa,wqb,eq.empty(),weqget))

def wq_put():
	global wg_ready,wqport,ip_g
	x=None
	try:
		x=next(ip_g)
		print('[wq_put]pid',os.getpid(),'x=',x)
	except:
		print('[wq_put]pid',os.getpid(),'x=None,ip_g is stop')
		wg_ready=False
		if not wg_ready and weqget:
			eq_get()
		else:
			return
	if x != None:
		x=(x,wqport)
		#print('[wq_put]x=',x)
		wq.put(x)
		return

async def work(loop):
	global opencount,closecount,ptime,st
	while True:
		addr=None
		con=''
		if not wq.empty():
			addr = wq.get()
			print('[work]addr:',addr)
			s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setblocking(0)
			try:
				con=await loop.sock_connect(s,addr)
			except OSError as err:
				closecount+=1
				err=str(err)
				std=std='%s,%s,%s\n\r'%(addr[0],addr[1],err)
				res_cache.append(std)
				#print('pid',os.getpid(),addr,err[12:31])
			if con == None:
				opencount+=1
				print('pid',os.getpid(),addr,'open')
				std='%s,%s,open\n\r'%(addr[0],addr[1])
				res_cache.append(std)
			s.close()
			ptime+=time.time()-st
			progress_count.value+=1
		elif weqget and wq.empty():
			wq_put()
		elif addr == None and not weqget:
			break
	return

def res_thread():
	global opencount,workers,res_cache
	print('[res_thread]res_thread tid',threading.current_thread().name,'is starting...')
	while True:
		if opencount%workers < workers/100:
			res_save()
		elif not weqget:
			while len(res_cache):
				res_save()
			break
		time.sleep(1)
	return

def res_save():
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

def pwfunc():
	global opencount,closecount,ptime
	#print('[pwfunc]pid-',os.getpid(),'is running...')
	state_pid.put(os.getpid())
	res_save_thread=threading.Thread(target=res_thread,name='res_thread_tid='+str(os.getpid()))
	res_save_thread.start()
	
	selloop=asyncio.SelectorEventLoop()
	asyncio.set_event_loop(selloop)
	loop = asyncio.get_event_loop()
	corus = prepare(workers,loop)
	fs=asyncio.gather(*corus)
	loop.run_until_complete(fs)
	loop.close()
	print('[pwfunc]ptime:',ptime)
	alltime.value+=ptime
	print('[pwfunc]alltime:',alltime.value)
	print('[pwfunc]allcount:',allcount.value)
	allcount.value+=opencount+closecount
	
	res_save_thread.join()
	ee.clear()
	ee.wait()
	
	#print('\ntracemalloc:',tracemalloc.get_traced_memory())
	print('[pwfunc]pid='+str(os.getpid())+' real time: '+str(ptime)+'s\topen_counts:'+str(opencount)+'\tclose_counts:'+str(closecount))
	print('[pwfunc]pid='+str(os.getpid())+' wfunc is done use time:%.4f' % (time.time()-st)+'s'+'\n[pwfunc]pid='+str(os.getpid())+' wq empty :',wq.empty(),'| errlist count :',len(errlist))
	while len(errlist):
		reslog.write('err:\t'+errlist.pop())
		reslog.flush()
	return os.getpid()

def cb_w_p_fin(test):
	global p_fin_c,procs
	p_fin_c.append(test)
	#print('[cb_w_p_fin]',p_fin_c)
	if len(p_fin_c) == procs:
		pwfunc.terminate()
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
	print('[prepare]pid-%s workers is ready'%os.getpid())
	return corus
###################################################################
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
	if type(procs) != int and procs > (os.cpu_count()*16):
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
		print("the ip range start ",ipseed[0]," counts ",ipcounts)
		return ipcounts,pe-ps+1,1,1,workers,procs,ps,pe,sp,host,ip
	elif ip and portlist:
		print("ip range :",ip)
		ipseed=iprange_g.set_seed(ip)
		ipcounts=iprange_g.ip_counts(ipseed)
		print("the ip range start ",ipseed[0]," counts ",ipcounts)
		return ipcounts,len(sp),1,0,workers,procs,ps,pe,sp,host,ip
	elif host and port:
		print("ip range :",host)
		return len(host),pe-ps+1,0,1,workers,procs,ps,pe,sp,host,ip
	elif host and portlist:
		print("ip range :",host)
		return len(host),len(sp),0,0,workers,procs,ps,pe,sp,host,ip
	else:
		print("please set ipaddr/port numbers or range")
		sys.exit(0)

if __name__=='__main__':
	alltask,ports,check_ip,check_port,workers,procs,ps,pe,sp,host,ipr=check_input()
	print('[mian]alltask:%s ports:%s check_ip:%s check_port:%s'%(alltask,ports,check_ip,check_port))
	tracemalloc.start()
	st=time.time()
	delcache()

#public var set
	#procs=os.cpu_count()
	wqs=workers
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
	wq=queue.Queue(int(wqs*procs))
	weqget=True
	wg=None
	ip_g=None
	wqport=None
	wg_ready=False
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
	ee.set()
	p_wfunc.join()
	print('\n[main]all works done,saved to %s'%fname)
	reslog.close()
	print('\nResult of Execution :')
	print('\nprocs : %s\tcorus : %s\tqueue maxsize : %s' % (procs,workers,wq.maxsize))
	print('real time: %.4f'%ptime,'open_counts:',opencount,'close_count:',closecount,'all counts',opencount+closecount)
	print('use time: %.4f' % (time.time()-st)+'s')