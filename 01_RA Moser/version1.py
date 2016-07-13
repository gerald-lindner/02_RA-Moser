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
import os
import sys
import base64
import csv,cStringIO,codecs
import twisted

from scrapy.crawler import CrawlerProcess #neccassary? test at time
#geld=0
#name=0
#number=0
#date=0
class moseritem(scrapy.Item):
    geld = scrapy.Field()
    name=scrapy.Field()
    number=scrapy.Field()
    date=scrapy.Field()
path3 = os.path.join(os.path.expanduser('~'), 'Documents', 'output.csv')
path4 = os.path.join(os.path.expanduser('~'), 'Documents', 'links.csv')
import csv #load csv into x
with(open(path4)) as csvfile:
    reader=csv.reader(csvfile,delimiter=';')
    for row in reader:
        x=row
geld=[]
name=[]
number=[]
date=[]
address=[]
town_to=[]#town together
town=[]#town alone
zip=[]
country=[]
class ramoser(scrapy.Spider): #scrapy class, contains everything
    name = 'ramoser'
    start_urls = x
    def parse(self,response):
        try: 
            geld_v=response.xpath('//strong/text()')[15].extract()
            geld_v=geld_v.replace('\r', '')
            geld_v=geld_v.replace("'", '')
            geld_v=geld_v.replace('\n', '')
            geld.append(geld_v)
        except: geld.append("NA")
        try:
            name_v=response.xpath('//strong/text()')[4].extract()
            name_v=name_v.replace('\r', '')
            name_v=name_v.replace('"', '')
            name_v=name_v.replace('\n', '')
            name_v=name_v.replace('*', '')
            name_v=name_v.replace('            ','')
            name.append(name_v)
        except: name.append("NA")
        try:
            address_v=response.xpath('//strong/text()')[5].extract()
            address.append(address_v)
        except: address.append("NA")
        try:
            town_to=response.xpath('//strong/text()')[6].extract()
            town_to=town_to.split(" ",1)#only one time
            town.append(town_to[1])
            zip.append(town_to[0])
        except:
            zip.append("NA")
            town.append("NA")
        try:
            number_v=response.xpath('//strong/text()')[8].extract()
            number_v=number_v.split(":")
            number.append(number_v[1])
        except: number.append("NA")
        try:
            country_v=response.xpath('//strong/text()')[7].extract()
            country_v=country_v.replace('\r', '')
            country_v=country_v.replace('"', '')
            country_v=country_v.replace('\n', '')
            country_v=country_v.replace('*', '')
            country.append(country_v)
        except:country.append("NA")
        try:
            date_v=response.xpath('//span/text()')[4].extract()
            date.append(date_v)
        except:
            date.append("NA")
            
process = CrawlerProcess()
process.crawl(ramoser)
process.start()

class UnicodeWriter:#simply to make utf-8 work
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


with open(path3,'wb') as fout:
    writer = UnicodeWriter(fout)
    writer.writerow(name)
    writer.writerow(address)
    writer.writerow(zip)
    writer.writerow(town)
    writer.writerow(country)
    writer.writerow(number)
    writer.writerow(geld)
    writer.writerow(date)

