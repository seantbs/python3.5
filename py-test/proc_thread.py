#!/usr/bin/python3

from multiprocessing import Process,Pool,Value,Array
import os,sys,io,threading,time,random,queue,logging

print("start time:",time.ctime())
st=time.time()

def check(s):
	print("check",threading.current_thread().name,"s =",s)
	for i in chk:
		print("chk[%i]=%i"%(i,i))
	chk.append(s)
	for i in chk:
		print("append then chk[%i]=%i"%(i,i))
	if chk[0] == chk[1]:
		print(threading.current_thread().name,"pts =",chk[0])
		pq_put()
	else:
		return 1
def g(s,e):
	if check(s):
		pts.value=pts.value+1
		for i in range(s,e):
			#print(threading.current_thread().name,"of g=",i)
			yield i

def pq_put():
	global pq
	for i in range(pts.value,pte.value):
		pg=g(i,i+1)
		try:
			pq.put(next(pg))
		except:
			break
		print("pq_put of",threading.current_thread().name,"=",pts.value)

def res(ramf):
	with open('./result.txt','a') as f:
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
	print("tfunc",threading.current_thread().name,"pts =",pts.value)
	while not pq.empty():
		ramf.write(threading.current_thread().name+" of is running.code =\t"+str(pq.get())+"\n")
		print(threading.current_thread().name,"is running.code =\t",pq.get())
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
	try:
		os.remove('./result.txt')
	except:
		pass
	os.mknod('./result.txt')

	pts=Value('i',ports)
	pte=Value('i',porte)
	chk=Array('i',[0,0])
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
