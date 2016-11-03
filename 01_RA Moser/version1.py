'''
Created on 13. Juli 2016

@author: geri
'''
#new start on 13. July 2016
#next: either enter extract_lunks here to get out name data, etc, or import everything from links
# some names are wrong, either because of " or of some other sign
#extract links from file rather than csv; get rid of that

#in default_settings.py
import scrapy #the crawler import
import re #for finding patterns
import os #for paths
#import sys
#import base64
#import csv
#import twisted
from scrapy.crawler import CrawlerProcess #neccassary? test at time
import pandas as pd

#paths
path1 = os.path.join(os.path.expanduser('~'), 'Documents', 'links.txt')
path2 = os.path.join(os.path.expanduser('~'), 'Documents', 'names.txt')
path3 = os.path.join(os.path.expanduser('~'), 'Documents', 'names.xlsx')
path4 = os.path.join(os.path.expanduser('~'), 'Documents', 'links.xlsx')

#read files
txt = open(path1,'r')
text1=txt.read()
txt2 = open(path2,'r')
text2=txt2.read()

#create patterns
pattern1= "Rechung =C3=B6ffnen <(.*\n.*)"
pattern2='Subject.*\n(.*)\n\n(.*)\n(.*)\n(.*)'

#create dataframe
columns = ['Name','Adresse', 'PLZ','Staat']
data_names=pd.DataFrame(columns=columns)


#m1,pattern1=hyperlinks, m2,pattern2=names
m1 = re.findall(pattern1,text1)
m1 = [w.replace('\n', '') for w in m1]
m1 = [w.replace('3D', '') for w in m1]
m1 = [w.replace('>=20', '') for w in m1]
m1= [w.replace('re_e=uro=1','re_euro=1')for w in m1]

m2=re.findall(pattern2,text2)

#create dataframe for names, double check with data_money
for x in range (0,len(m2)):
    data_names.loc[x]=[m2[x][0],m2[x][1],m2[x][2],m2[x][3]]
    x+=1
#must be a better way to do this
op1=[]
op2=[]
op3=[]
op4=[]
op5=[]
op6=[]
op7=[]
op8=[]
op9=[]
class ramoser(scrapy.Spider): #scrapy class, contains everything
    name = 'ramoser'
    start_urls = m1[0:len(m1)] #for experiment reasosn
    def parse(self,response):
        try: #here i still have the problem of not getting spaces out
            name_v=response.xpath('//strong/text()')[4].extract()
            name_v=name_v.strip()
            name_v=name_v.replace('\r', '')
            name_v=name_v.replace('"', '')
            name_v=name_v.replace('\n', '')
            name_v=name_v.replace('*', '')
            print(name_v)
            op1.append(name_v)
        except: 
            op1.append("NA")
        
        try:
            address_v=response.xpath('//strong/text()')[5].extract()
            op2.append(address_v)
        except: 
            op2.append("NA")
        
        try:
            town_to=response.xpath('//strong/text()')[6].extract()
            town_to2=town_to.split(" ",1)#only one time
            op3.append(town_to2[0])
            op4.append(town_to2[1])
            op5.append(town_to)
        except:
            op3.append("NA")
            op4.append("NA")
            op5.append("NA")
            
        try:
            country_v=response.xpath('//strong/text()')[7].extract()
            country_v=country_v.replace('\r', '')
            country_v=country_v.replace('"', '')
            country_v=country_v.replace('\n', '')
            country_v=country_v.replace('*', '')
            op6.append(country_v)
        except:
            op6.append("NA")
        
        try:
            number_v=response.xpath('//strong/text()')[8].extract()
            number_v=number_v.split(":")
            op7.append(number_v[1])
        except: 
            op7.append("NA")
            
        try: 
            geld_v=response.xpath('//strong/text()')[15].extract()
            geld_v=geld_v.replace('\r', '')
            geld_v=geld_v.replace("'", '')
            geld_v=geld_v.replace('\n', '')
            op8.append(geld_v)
        except: 
            op8.append("NA")
            
        try:
            date_v=response.xpath('//span/text()')[4].extract()
            date_v=date_v.replace('\r', '')
            date_v=date_v.replace('\n', '')
            op9.append(date_v)
        except:
            op9.append("NA")


         
process = CrawlerProcess()
process.crawl(ramoser)
process.start()
#dataframe for crawling results
columns2 = ['Name','Adresse', 'PLZ','Ort','Adresse und PLZ','Staat','Nummer',"Geld",'Datum']
data_money=pd.DataFrame(columns=columns2)
for i in range(0,len(op1)):
    all=data_money.loc[i]=[op1[i],op2[i],op3[i],op4[i],op5[i],op6[i],op7[i],op8[i],op9[i]]
    data_money.append(all)

writer = pd.ExcelWriter(path3)
data_money.to_excel(writer,'Sheet1')
writer.save()

