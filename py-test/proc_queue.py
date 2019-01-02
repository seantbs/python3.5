#!/usr/bin/python3.5

from multiprocessing import Process,Pool,Queue,Value,Array
import os,threading,queue,time,random
print("start running:",time.ctime())

def pa_y():
  for i in range(pa.value,pb):
    yield i

def pw_y(a):
  while not pw.full():
    for i in range(a):
      i=i*2
      pw.put(i)
  return

def tq_y(a,b):
  for i in range(a,b):
    yield i

def check(w):
  #print("put proc id=",os.getpid(),"pa value:",pa.value)
  #print(os.getpid(),"pq empty:",pq.empty())
  if pa.value >= pb:
    return 0
  elif pq.empty():
    pq.put(w)
    #print("put proc id=",os.getpid(),"weight code:",w)
    return 1
  else:
    tfunc(w)

def tq_put(w):
  print(threading.current_thread().name,"pa value:",pa.value)
  if check(w) and pa.value < pb:
    pc=pa_y()
    pg=tq_y(next(pc),pb)
    while not tq.full():
      try:
        tq.put(next(pg))
        pa.value=next(pc)
      except:
        return
    pq.get()
    #print("get proc id=",os.getpid(),"weight code:",pq.get())
    tfunc(w)
  else:
    return

def pfunc(pv,ths):
  w=pw.get()
  print("pfunc that pid=",os.getpid(),"is runcode=",pv,"wcode=",w)
  thpool=[]
  for i in range(ths):
      t=threading.Thread(target=tfunc,args=(w,),name="tid"+str(os.getpid())+r"/"+str(i))
      thpool.append(t)
  for a in thpool:
      a.start()
  for b in thpool:
      b.join()

def tfunc(w):
  #print(threading.current_thread().name,"tq empty is",tq.empty())
  while not tq.empty():
    print("tfunc that",threading.current_thread().name,"is running code=\t",tq.get())
    time.sleep(random.randint(1,2))
  tq_put(w)

if __name__=='__main__':
  tstart=time.time()
  pv=123456
  procs=os.cpu_count()
  ths=10
  tq=queue.Queue(ths)

  pa=Value('i',1)
  pb=101
  pw=Queue(procs)
  pw_y(procs)
  pq=Queue(2)

  p=Pool(procs)
  for i in range(procs):
    p.apply_async(pfunc,args=(pv,ths,))
  p.close()
  p.join()
  tend=time.time()
  print("real time:",tend-tstart)
