#!/usr/bin/python3

import sys,io,time,pgbar

st=time.time()

f=open('./result.log','r+')
t1=f.readlines()
t2=[]
t3=[]
allc=int(input('input allc =:'))
err=[]
r=[]
acc=0

for i in range(allc):
	t2.append(i+1)
	if (i+1)%(allc/1000) == 0 and (i+1) < allc:
		time.sleep(0.01)
		sys.stdout.write('\rfill list t2...'+str(i+1))
		sys.stdout.flush()
	elif (i+1) == allc:
		sys.stdout.write('\rfill list t2...'+str(i+1)+'\n')

print('\nrunning:')

for i in t2:
	r=[]
	c=0
	pgbar.ratio(allc,i,1000)
	for ii in t1:
		if i == int(ii):
			c+=1
			r.append(i)
			r.append(c)
			t3.append(r)
			allc+=1
			t1.remove(ii)
	if c == 0:
		err.append(i)
	elif c > 1:
		err.append(i)

print('\nt1 count:',len(t1),'\nt2 count:',len(t3),'\nerr count:',len(err),'\n')
print('use time :',time.time()-st,'s')
