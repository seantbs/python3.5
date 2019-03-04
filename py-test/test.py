import asyncio,sys,time,queue,random,os
import threading,multiprocessing

#test future
async def slow_operation(future):
	print('[fun]Future is done!')
	await wait_time(1)
	future.set_result('\nFuture is done!')

async def wait_time(t):
	for i in range(100):
		sys.stdout.write('\rwait...'+str(i+1)+'%')
		time.sleep(t/100)

def got_result(future):
    print(future.result())
    loop.stop()
####################################################################
#test loop
async def work():
	global ct,cw,res_cache,workers
	while True:
		std = ''
		text = ''
		x = None
		r = random.randint(2,6)
		if not wq.empty():
			x = wq.get()
			ct+=r
			cw+=1
			print('[work_%s]work %s is running...' % (x,x))
			for i in range(r):
				text+='a'
				await asyncio.sleep(1)
			std=str(x)+'\t'+text+'\n'
			print('[work_%s]x = %s,r = %s,std = %s' % (x,x,r,std))
			res_cache.append(std)
			if cw%(workers) < workers/100:
				await res_save()
		else:
			while len(res_cache):
				await res_save()
			return

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

def wq_put_y(a):
	for i in range(a):
		yield i+1

def workers_y(a):
	for i in range(a)
		yield work()

def wq_put():
	global wq_g
	while True:
		try:
			x = next(wq_g)
		except:
			coro_tasks()
		wq.put(x)

def coro_tasks():
	global coros,workers_g
	while True:
		try:
			x = next(workers_g)
		except:
			return
		coros.append(x)

def run_threads(ths):
	thp=[]
	for i in range(ths):
		t=threading.Thread(target=wq_put,name='tid'+str(os.getpid())+r'/'+str(i))
		thp.append(t)
	for a in thp:
		a.start()
	for b in thp:
		b.join()
	print('[run_threads]wq is ready...')

if __name__=='__main__':
	st=time.time()
	
	fname='./test.log'
	try:
		os.remove(fname)
	except:
		pass
	os.path.exists(fname)
	reslog=open(fname,'a')
	
	ct=0
	cw=0
	res_cache=[]
	workers=10450
	counts=66000
	ths=1500
	coros=[]
	workers_g=worker_y(worker)
	wq_g=wq_put_y(counts)
	wq=queue.Queue()
	
	run_threads(ths)
	
	loop = asyncio.get_event_loop()
	fs=asyncio.gather(*coros)
	loop.run_until_complete(fs)
	loop.close()
	print('no work to do...',wq.qsize())
	reslog.close()
	
	print('real time : %s\tcounts : %s' % (ct,cw))
	print('use time:%.4f'%(time.time()-st))
	