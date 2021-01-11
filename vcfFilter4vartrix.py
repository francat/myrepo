#coding:utf-8

import sys
import re
import os

f1=open(sys.argv[1],'r')#SF11232_2.hg38_multianno.txt_nonsy.vcf
f2=open(sys.argv[2],'w')

for i in f1:
    i=i.strip()
    h=i.split('	')
    m=re.match('#',i)
    if m is not None:
        print >>f2,i
    if m is None:
        if '1/1' not in h[-2]:
            j=h[-1].split(':')
            if int(j[2])>10:
                print >>f2,i
f1.close()
f2.close()
