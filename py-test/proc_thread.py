#!/usr/bin/python3

from multiprocessing import Process,Pool,Value
import os,sys,io,threading,time,random,queue,logging

print("start time:",time.ctime())
st=time.time()

def g(s,e):
	pts.value=pts.value+1
	for i in range(s,e):
		#print(threading.current_thread().name,"of g=",i)
		yield i

def pq_put():
	global pq
	for i in range(pts.value,pte.value):
		if pts.value == i and pts.value < pte.value:
			pg=g(pts.value,pts.value+1)
			try:
				pq.put(next(pg))
			except:
				break
		elif pts.value != i:
		#print("pq_put of",threading.current_thread().name,"=",pts.value)

def res(ramf):
	print(ramf)
	with open('./test.txt','w') as f:
		f.write(ramf)

def pfunc(pcode,ths):
	print(os.getpid(),"is running.code =",pcode)
	thpool=[]
	for i in range(ths):
		t = threading.Thread(target=tfunc,args=(),name="threadid-"+str(os.getpid())+r"/"+str(i))
		thpool.append(t)
	for a in thpool:
		a.start()
	for b in thpool:
		b.join()

def tfunc():
	while not pq.empty():
		ramf.write(threading.current_thread().name+" of is running.code =\t"+str(pq.get())+"\n")
		#time.sleep(0.01)
		#print(threading.current_thread().name,"is running.code =\t",pq.get())
		r=random.randint(1,2)
		time.sleep(r)
	pq_put()
	res(ramf.getvalue())

if __name__=='__main__':
	pcode=123456
	procs=2
	ths=10
	ports=1
	porte=101

	ramf=io.StringIO()
	os.remove('./test.txt')
	os.mknod('./test.txt')
	pts=Value('i',ports)
	pte=Value('i',porte)
	print("pts.value=%i,pte.value=%i"%(pts.value,pte.value))
	pq=queue.Queue(ths)
	
	print("="*60)
	print('Parent process %s.' % os.getppid())
	print("="*60)
	p=Pool(procs)
	for i in range(procs):
		p.apply_async(pfunc,args=(pcode,ths,))
	p.close()
	p.join()
	
	print("real time:",time.time()-st)
	print("main process",os.getppid(),"(child process:",os.getpid(),") end.")

	print("end time:",time.ctime())

