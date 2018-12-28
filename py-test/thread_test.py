#!/usr/bin/python3

import sys,time,threading,argparse

parser=argparse.ArgumentParser(description='input threads number value that you need .')
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
parser.add_argument('-ths',type=int,nargs='?',default=4,help='set threads number value.the default value is 4 threads.')
parser.parse_args()
args=parser.parse_args()

print("start test:",time.ctime())

#create generator
def prange_test(a):
        i=0
        while i<a:
                i=i+1
                yield i

#create test func include lock and event
def pg(y):
	global p
	while p!=0:
		event.set()
		try:
			print(threading.current_thread().name,"handle port ",next(y))
			time.sleep(1)
		except:
			break
		plock.acquire()
		p=p-1
		print("new p value =",p)
		plock.release()
		event.wait()


#main pg
#define generator
p=20
test=prange_test(p)

#check ths args.ths value
def check_ths(t,p):
	if t > (p*0.01) or t > 1024:
		t=int(p*0.01)+1
		print(t)
		print("just %d ports will be scaned.but you want to set threads %d !? are you sure? seriously? maybe %d threads will be enough." % (p,args.ths,t))
	elif p < 4:
		t=p
		print(t)
	return t

#ths=check_ths(args.ths,p)
ths=args.ths

#create event object and threads pool
thpool=[]
event=threading.Event()
plock=threading.Lock()
for i in range(ths):
	tname="threadID"+str(i+1)
	th = threading.Thread(target=pg,args=(test,),name=tname)
	thpool.append(th)
	#print(thpool)

#start threads
for th in thpool:
	th.start()

#wait and end threads
for th in thpool:
	th.join()
	print('%d threads are running...' % threading.active_count())

print('thread %s ended.' % threading.current_thread().name)
print('end threads time:',time.ctime())
