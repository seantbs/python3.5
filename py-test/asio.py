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

async def compute(x, y):
	print("Compute %s + %s ..." % (x, y))
	await asyncio.sleep(1.0)
	return x + y

async def print_sum(x, y):
	result = await compute(x, y)
	print("%s + %s = %s" % (x, y, result))

###########################################################
'''async def wq_put():
	global i,st
	while True:
		i+=1
		print('[wq_put]i =',i,'<->',time.time()-st)
		wq.put(i)
		await asyncio.sleep(1)
		if i < 5:
			continue
		else:
			return

async def wq_get():
	global text
	print('wq get is starting...')
	while not wq.empty():
		text=''
		try:
			x=str(wq.get())
		except:
			await wq_put()
		print('[wq_get]x =',x)
		r=random.randint(2,8)
		for i in range(r):
			text+='a'
			await asyncio.sleep(1)
		print('[wq_get]text : '+x+','+text)'''

if __name__ == '__main__':
	st=time.time()
	
	'''i=0
	text=''
	wq=queue.Queue(4)
	
	#coroutine test
	c = consumer()
	produce(c)'''
	
	loop = asyncio.get_event_loop()
	loop.run_until_complete(print_sum(1, 2))
	loop.close()

	'''loop = asyncio.get_event_loop()
	astks = [wq_get(),wq_put()]
	loop.run_until_complete(asyncio.wait(astks))
	loop.close()'''
	
	print('use time: %.3f ' % (time.time()-st)+'s')
