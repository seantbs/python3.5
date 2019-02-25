import asyncio,sys,time

async def slow_operation(future):
	print('[fun]Future is done!')
	await wait_time(1)
	future.set_result('\nFuture is done!')

async def wait_time(t):
	for i in range(100):
		sys.stdout.write('\rwait...'+str(i+1)+'%')
		time.sleep(t/100)

def got_result(future):
    print(future.result())
    loop.stop()

if __name__=='__main__':
	st=time.time()
	loop = asyncio.get_event_loop()
	future = asyncio.Future()
	asyncio.ensure_future(slow_operation(future))
	loop.run_until_complete(future)
	'''print(future.result())
	loop.close()'''
	future.add_done_callback(got_result)
	try:
		loop.run_forever()
	finally:
		loop.close()

	print('use time:%.4f'%(time.time()-st))