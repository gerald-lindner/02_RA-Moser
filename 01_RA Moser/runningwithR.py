#! /usr/bin/python
#-*- coding: utf-8 -*-
'''
Created on 31.08.2015

@author: geri
'''
#First, copy mail content (not original) into names.txt, delete it first
#Second, copy mail original into links.txt
#Third: Run, transpose links and do R: merge files
#You're Done HERE mate!
from sys import argv
import re 
import os
from csv import Dialect, excel
import csv

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


path = os.path.join(os.path.expanduser('~'), 'Documents', 'links.txt')
path2 = os.path.join(os.path.expanduser('~'), 'Documents', 'names.txt')
path3 = os.path.join(os.path.expanduser('~'), 'Documents', 'names.csv')
path4 = os.path.join(os.path.expanduser('~'), 'Documents', 'links.csv')

txt = open(path,'r')
text=txt.read()
txt2 = open(path2,'r')
text2=txt2.read()
pattern= "Rechung =C3=B6ffnen =\n<(.*\n.*)"
pattern2='Subject.*\n(.*)\n\n(.*)\n(.*)\n(.*)'

#data_names=pd.DataFrame(columns=[])



m = re.findall(pattern,text)
m = [w.replace('\n', '') for w in m]
m = [w.replace('3D', '') for w in m]
m = [w.replace('>=20', '') for w in m]
m= [w.replace('re_e=uro=1','re_euro=1')for w in m]
m2=re.findall(pattern2,text2)
#m = [w.replace('\n', '') for w in m]
print(m2[5])
l=[]
for x in range (0,len(m2)):
    import csv
    with open(path3,'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(m2[x])
    x=x+1
import csv
unicode_csv_reader(path3)
   
import csv
with open(path4,'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';')
    spamwriter.writerow(m)
