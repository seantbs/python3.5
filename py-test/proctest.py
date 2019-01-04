#!/usr/bin/python3.5

from multiprocessing import Pool,Queue,Value,Event
import os,threading,queue,time,random

print("start running:",time.ctime())

def pq_y():
	global procs,ths
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
	global pb,w
	print("put proc id=",os.getpid(),"weight code:",w)
	if pa.value >= pb:
		return 0
	elif pq.empty():
		g=pq_y()
		pq.put(next(g))
		print("put proc id=",os.getpid(),"pa value:",pa.value)
		return 1

def tq_put():
	global ths
	a,b=0,0
	print(threading.current_thread().name,"is prepare pa value:",pa.value)
	try:
		b=pq.get_nowait()
		tevent.clear()
		a=b-ths
		print("get proc id=",os.getpid(),"pq get:",a)
	except:
		pass
	g=tq_y(a,b)
	while not tq.full():
		try:
			tq.put(next(g))
			a+=a+1
		except:
			return
	tfunc()

def pfunc():
	global pcode,w
	w=pw.get()
	print("pfunc that pid=",os.getpid(),"ppid is",os.getppid(),"is runcode=",pcode,"wcode=",w)
	c_event_th()
	c_work_th()

def tfunc():
	print(threading.current_thread().name,"tq empty is",tq.empty())
	while not tq.empty():
		print("tfunc that",threading.current_thread().name,"is running =",tq.get())
		time.sleep(random.randint(1,2))
	tevent.wait()
	tq_put()

def efunc():
	print(threading.current_thread().name,"is running.")
	while tevent.is_set() == False:
		check()
		tevent.set()

def c_proc(procs):
	p=Pool(procs)
	for i in range(procs):
		p.apply_async(pfunc,args=())
	p.close()
	p.join()
	
def c_work_th():
	global ths
	thpool=[]
	for i in range(ths):
		t=threading.Thread(target=tfunc,args=(),name="tid"+str(os.getpid())+r"/"+str(i))
		thpool.append(t)
	for a in thpool:
		a.start()
	for b in thpool:
		b.join()

def c_event_th():
	print('event thread is starting...')
	te=threading.Thread(target=efunc,args=(),name="event_tid-"+str(os.getpid()))
	te.start()
	te.join()

if __name__=='__main__':
	stime=time.time()
	pcode='ABCD'
	procs=2
	ths=4
	pcode=123456
	tq=queue.Queue(ths)
	
	pa=Value('i',1)
	pb=31
	w=0
	pw=Queue(procs)
	pw_y(procs)
	pq=Queue(procs)
	
	pevent=Event()
	tevent=threading.Event()
	c_proc(procs)

	print("real time:",time.time()-stime)
	print("end time:",time.ctime())
