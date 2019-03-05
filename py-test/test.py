import asyncio,sys,time,queue,random,os
import threading,multiprocessing,pgbar

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
	global ct,cw,res_cache,workers,works
	while True:
		std = ''
		text = ''
		x = None
		r = random.randint(2,6)
		if not wq.empty():
			x = wq.get()
			ct+=r
			cw+=1
			if cw%1000 == 0:
				pgbar.bar(works,cw,50,st)
			elif cw == works:
				pgbar.bar(works,cw,50,st)
			#print('[work_%s]work %s is running...' % (x,x))
			for i in range(r):
				text+='a'
				await asyncio.sleep(1)
			std=str(x)+'\t'+text+'\n'
			#print('[work_%s]x = %s,r = %s,std = %s' % (x,x,r,std))
			res_cache.append(std)
			if cw%1000 == 0:
				pgbar.bar(works,cw,50,st)
			elif cw == works:
				pgbar.bar(works,cw,50,st)
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
	for i in range(a):
		yield work()

def prepare(workers,counts):
	print('[prepare]prepare workers...')
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
	print('\n[prepare]workers is ready')
	
	print('[prepare]prepare wq...')
	count=0
	wq_g=wq_put_y(works)
	while True:
		try:
			x = next(wq_g)
		except:
			break
		wq.put(x)
		count+=1
		if count%1000 == 0:
			pgbar.bar(works,count,50,st)
		elif count==works:
			pgbar.bar(works,count,50,st)
	print('\n[prepare]wq is ready')
	return coros

def run_threads(workers,counts):
	t1=threading.Thread(target=prepare,args=(workers,works),name='tid'+str(os.getpid())+'t1')
	t1.start()
	t1.join()
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
	workers=10000
	works=65536
	wq=queue.Queue()
	coros = prepare(workers,works)

	print('working....')
	loop = asyncio.get_event_loop()
	fs=asyncio.gather(*coros)
	loop.run_until_complete(fs)
	loop.close()
	reslog.close()
	print('\nno work to do...',wq.qsize())
	
	print('real time : %s\tcounts : %s' % (ct,cw))
	print('use time:%.4f'%(time.time()-st))
	