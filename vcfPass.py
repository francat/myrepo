#coding:utf-8

import sys
import re
import os

f1=open(sys.argv[1],'r')
f2=open(sys.argv[2],'w')


for i in f1:
    i=i.strip()
    h=i.split()
    #j=h[0].split('_added_sorted.MarkD.split')
    m=re.match('#',i)
    if m is not None:
        print >>f2,i
    if m is None:
        if 'PASS' in h[6]:
            print >>f2,i

f1.close()
f2.close()
