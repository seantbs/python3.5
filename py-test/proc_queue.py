#!/usr/bin/python3.5

from multiprocessing import Process,Pool,Queue,Value,Array
import os,threading,queue,time,random
print("start running:",time.ctime())

def pq_y(procs):
	global ths
	for i in range(procs):
		if pb-pa.value>=ths:
			ct=pa.value+ths
			pa.value=ct
			yield ct
		else:
			yield pb

def pw_y(a):
	while not pw.full():
		for i in range(a):
			i=i*2
			pw.put(i)
	return

def tq_y(a,b):
	for i in range(a,b):
		yield i

def check():
	global procs
	#print("put proc id=",os.getpid(),"pa value:",pa.value)
	if pa.value >= pb:
		return 0
	elif pq.empty():
		g=pq_y(procs)
		pq.put(next(g))
		#print("put proc id=",os.getpid(),"weight code:",w)
		return 1

def tq_put():
	global ths
	pevent.set()
	pevent.wait()
	print(threading.current_thread().name,"pa value:",pa.value)
	if check(w) and pa.value < pb:
	    a=pq.get()
		pevent.set()
		g=tq_y(a-ths,a)
		while not tq.full():
			try:
				tq.put(next(g))
			except:
				return
		#print("get proc id=",os.getpid(),"weight code:",pq.get())
		tfunc()
	else:
		return

def pfunc(pv,ths):
	global ths,w
	if w == 0:
		create_ths(ths)
		w=pw.get()
		print("pfunc that pid=",os.getpid(),"is runcode=",pv,"wcode=",w)
	check()

def create_ths(ths):
	thpool=[]
	for i in range(ths):
			t=threading.Thread(target=tfunc,args=(),name="tid"+str(os.getpid())+r"/"+str(i))
			thpool.append(t)
	for a in thpool:
			a.start()
	for b in thpool:
			b.join()

def tfunc():
	#print(threading.current_thread().name,"tq empty is",tq.empty())
	while not tq.empty():
		print("tfunc that",threading.current_thread().name,"is running code=\t",tq.get())
		time.sleep(random.randint(1,2))
	tq_put()

if __name__=='__main__':
	tstart=time.time()
	pv=123456
	procs=os.cpu_count()
	ths=8
	tq=queue.Queue(ths)

	pa=Value('i',1)
	pb=101
	
	w=0
	pw=Queue(procs)
	pw_y(procs)
	
	pq=Queue(procs)

	p=Pool(procs)
	for i in range(procs):
		p.apply_async(pfunc,args=(pv,ths,))
	p.close()
	p.join()
	tend=time.time()
	print("real time:",tend-tstart)
