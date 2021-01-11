#coding:utf-8
 
import sys
import re
import os

f1=open(sys.argv[1],'r')
f2=open(sys.argv[2],'r')
f3=open(sys.argv[3],'w')

s=[]
t={}
for i in f1:
    i=i.strip()
    h=i.split()
    s.append(h[0]+'_'+h[1])

for i in f2:
    i=i.strip()
    h=i.split()
    m=re.match('#',i)
    if m is not None:
        print >>f3,i
    if m is None:
        if h[0]+'_'+h[1] in s:
            print >>f3,i

f1.close()
f2.close()
f3.close()
