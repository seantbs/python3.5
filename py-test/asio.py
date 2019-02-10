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
		print('work',n,'...',i+1)
		await asyncio.sleep(1)
	return

if __name__ == '__main__':
	st=time.time()
	
	'''i=0
	text=''
	wq=queue.Queue(4)
	
	#coroutine test
	c = consumer()
	produce(c)'''
	wq=queue.Queue()
	for i in range(100):
		wq.put(i+1)
	y=0
	loop = asyncio.get_event_loop()
	astks=[work(i) for i in range(3)]
	loop.run_until_complete(asyncio.wait(astks))
	loop.close()

	'''loop = asyncio.get_event_loop()
	astks = [wq_get(),wq_put()]
	loop.run_until_complete(asyncio.wait(astks))
	loop.close()'''
	
	print('use time: %.3f ' % (time.time()-st)+'s')
