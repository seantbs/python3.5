#!/usr/bin/python3.5

import socket,time,os,sys,asyncio,queue

async def work(host,loop):
	global opencount,closecount,ptime
	while not wq.empty():
		addr=wq.get()
		con=''
		st=time.time()
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setblocking(0)
		#print('[work]host:',i,s)
		try:
			con=await loop.sock_connect(s,addr)
		except OSError as err:
			closecount+=1
			err=str(err)
			#print(addr,err[12:31])
		if con == None:
			opencount+=1
			print(addr,'open')
		s.close()
		ptime+=time.time()-st
		#print('[work]ptime=',ptime)

def workers_y(a,host,loop):
	for i in range(a):
		yield work(host,loop)

def prepare(workers,host,loop):
	count=0
	corus=[]
	workers_g=workers_y(workers,host,loop)
	while True:
		try:
			x = next(workers_g)
		except:
			break
		corus.append(x)
		count+=1
	return corus

if __name__=='__main__':
	st=time.time()
	ptime=0
	opencount=0
	closecount=0
	
	wq=queue.Queue()
	host=[]
	for i in range(1,65536):
		x='10.186.64.3'
		y=i
		z=(x,y)
		wq.put(z)
	
	workers=900
	selloop=asyncio.SelectorEventLoop()
	asyncio.set_event_loop(selloop)
	loop = asyncio.get_event_loop()
	corus = prepare(workers,host,loop)
	fs=asyncio.gather(*corus)
	loop.run_until_complete(fs)
	loop.close()
	print('real time: %.4f'%ptime,'open_counts:',opencount,'close_count:',closecount,'all counts',opencount+closecount)
	print("use time: %.4f"%(time.time()-st))