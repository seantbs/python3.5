#! /usr/bin/python3.5

import asyncio,time

def consumer():
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
	c.close()

if __name__ == '__main__':
	st=time.time()
	
	c = consumer()
	produce(c)
	
	print('use time: %.2f ' % (time.time()-st)+'s')

