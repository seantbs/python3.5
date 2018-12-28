#!/usr/bin/python3

from multiprocessing import Process,Pool,Queue
import os,sys,threading,time,random

print("start time:",time.ctime())
st=time.time()

def ty(s,e):
	if s != e:
		for i in range(s,e):
			i=i+1
			yield i
	else:
		print("yield is done.")
def q_put(g):
	if ports != porte:
		while not portq.full():
			try:
				portq.put(next(g))
				print("there are still",porte-ports,"to queue in",os.getpid())
			except:
				break
	else:
		print("there is nothing to queue.")

def ptest(pv,ths,test):
	print(os.getpid(),"is running.code =",pv)
	test=test+test
	thpool=[]
	for i in range(ths):
		t = threading.Thread(target=ttest,args=(),name="threadid-"+str(os.getpid())+r"/"+str(i))
		thpool.append(t)
		#print(threading.current_thread().name,"of",os.getpid(),"is appended.")
	print(test)
	for a in thpool:
		a.start()
		#print(threading.current_thread().name,"of",os.getppid(),"is starting.")
	for b in thpool:
		b.join()
		#print("thread",threading.current_thread().name,"of",os.getpid(),"is ended.")

def ttest():
	#print(threading.current_thread().name,"start time",time.time())
	while not portq.empty():
		print(threading.current_thread().name,"of",os.getpid(),"is running.code =",portq.get())
		r=random.randint(1,2)
		#print("user time:",r)
		time.sleep(r)

if __name__=='__main__':
	pv=123
	ps=2
	ths=2
	ports=0
	porte=20
	test=100
	portq=Queue(ps*ths)
	y=ty(ports,porte)
	q_put(y)

	print("="*60)
	print('Parent process %s.' % os.getppid())
	print("="*60)
	p=Pool(ps)
	for i in range(ps):
		p.apply_async(ptest,args=(pv,ths,test,))
	p.close()
	p.join()

	print("main process",os.getppid(),"(child process:",os.getpid(),") end.")
	print("real time:",time.time()-st)
	print("end time:",time.ctime())

