#!/usr/bin/python3

import sys,io,time,pgbar

st=time.time()

f=open('./result.log','r+')
t1=f.readlines()
t2=[]
t3=[]
allc=0
err=[]
r=[]
acc=0

for i in range(5000):
	t2.append(i+1)
	if (i+1)%300 == 0:
		time.sleep(0.1)
		sys.stdout.write('\rfill list t2...'+str(i+1))
		sys.stdout.flush()
	elif (i+1) == 5000:
		sys.stdout.write('\rfill list t2...'+str(i+1)+'\n')

print('\nrunning:')

for i in t2:
	r=[]
	c=0
	acc=pgbar.bar(0,5000,i,82,acc)
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
