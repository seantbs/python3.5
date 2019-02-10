#! /usr/bin/python3.5

import asyncio,time,queue,random

'''def consumer():
	r = ''
	while True:
		n = yield r
		if not n:
			return
		print('[CONSUMER] Consuming %s...' % n)
		r = '200 OK'

def produce(c):
	c.send(None)
	n = 0
	while n < 5:
		n = n + 1
		print('[PRODUCER] Producing %s...' % n)
		r = c.send(n)
		print('[PRODUCER] Consumer return: %s' % r)
	c.close()'''

###########################################################
async def work(n):
	for i in range(3):
		print('work',n,'...','count:',i+1)
		wq.put_nowait(i)
		t = await check()
		print('work',n,'t :',t)
		if t == 'ok':
			wq.put_nowait(i+1)
	return

async def check():
	c = await wq.get()
	print('[check]c =',c)
	await asyncio.sleep(1)
	return 'Ok'

def y():
	for i in range(3):
		yield i+1
		return

async def main():
	await asyncio.gather(work(1),work(2),work(3))

if __name__ == '__main__':
	st=time.time()
	
	'''i=0
	text=''
	wq=queue.Queue(4)
	
	#coroutine test
	c = consumer()
	produce(c)'''
	wq=asyncio.Queue()
	y=0
	asyncio.run(main())
	#loop = asyncio.get_event_loop()
	#astks=asyncio.create_task(work(i+1) for i in range(3))
	#loop.run_until_complete(asyncio.wait(astks))
	#loop.close()

	'''loop = asyncio.get_event_loop()
	astks = [wq_get(),wq_put()]
	loop.run_until_complete(asyncio.wait(astks))
	loop.close()'''
	
	print('use time: %.3f ' % (time.time()-st)+'s')
