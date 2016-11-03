'''
Created on 13. Juli 2016

@author: geri
'''
import scrapy #the crawler import
import re #for finding patterns
from scrapy.crawler import CrawlerProcess #neccassary? test at time
a=[]
class ramoser(scrapy.Spider): #scrapy class, contains everything
    name = 'ramoser'
    start_urls = ["http://www.upps.org/main/re.php?cl=39&id=288&l=no&p=wuejct6&re_euro=1&na=1"]
    def parse(self,response):
        name_v=response.xpath('//strong/text()')[4].extract()
        name_v=name_v.replace('\r', '')

        name_v=name_v.lstrip()
        name_v=name_v.replace('\n', '')
#             name_v=name_v.replace('*', '')
#             name_v=name_v.replace('            ','')
        a.append(name_v)
process = CrawlerProcess()
process.crawl(ramoser)
process.start()
print(a)