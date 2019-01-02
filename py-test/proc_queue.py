#!/usr/bin/python3.5

from multiprocessing import Process,Pool,Queue,Value,Array
import os,threading,queue,time,random

def y(a,b):
  for i in range(a,b):
    i=i+1
    yield i

def check():
  print("proc weight code:",w)
  try:
      q.put_nowait(w)
      return pa
  except:
      while q.empty():
          q.put_nowait(w)
      return pa


def pq_put():
  a=check()
  if check():
    pg=y(a,pe)
    while not pq.full():
      pq.put_nowait(next(pg))
      pa=pa+1
    q.get_nowait()

def pfunc(pv,ths):
  w=pw.pop()
  print("pfunc that pid=",os.getpid(),"is runcode=",pv,"wcode=",w)
  thpool=[]
  for i in range(ths):
      t=threading.Thread(target=tfunc,args=(),name="tid"+str(os.getpid())+r"/"+str(i))
      thpool.append(t)
  for a in thpool:
      a.start()
  for b in thpool:
      b.join()

def tfunc():
  while not pq.empty():
      print("tfunc that",threading.current_thread().name,"is running code=",pq.get())
      time.sleep(random.randint(1,2))
  pq_put()

if __name__=='__main__':
  tstart=time.time()
  pv=123456
  ps=2
  ths=4
  pw=[1,2]
  pa=Value("i",1)
  pb=Value("i",10)
    
  pq=queue.Queue(ths)
  q=Queue(1)
  p1=Process(target=pfunc,args=(pv,ths,),name="pid"+str(os.getpid()))
  p2=Process(target=pfunc,args=(pv,ths,),name="pid"+str(os.getpid()))
  p1.start()
  p2.start()
  p1.join()
  p2.join()
  #p=Pool(ps)
  #for i in range(ps):
  #  p=multiprocessing.apply_async(pfunc,args=(pv,ths,pq,ports,porte,))
  #p.close()
  #p.join()
  tend=time.time()
  print("real time:",tend-tstart)