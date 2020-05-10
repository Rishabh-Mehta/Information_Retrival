import numpy as np
import pandas as pd
import urllib.request
import urllib.error
from urllib.parse import urlparse
import re
import sys
import time
import logging



DATA_URL = 'https://cs.uic.edu'


def read_page(req):
    try:
        if(re.search('/$',req)):
            req=req[:-1]
        response = urllib.request.urlopen(req)
        content = response.getheader('Content-Type')
        if(re.match('text/html',content) or 
        re.match('text/plain',content) or 
        re.match('text/xml',content)):
          return response.read(),response
        else:
          return 0,0
    except urllib.error.HTTPError as e:
        #print('Error code: ', e.code,req)
        return 0,0
    except urllib.error.URLError as e:
        #print('Error code: ', e.reason,req)
        return 0,0
    except :
        #print ("Error",sys.exc_info()[0])
        return 0,0

def link_extraction_canonicalization(page,response):
  url=[]
  out=[]
  links=re.finditer("<a.*?href=\"(.*?)\".*?<\/?a>",str(page))
  for link in links:
    req=link.group(1)
    req=re.sub(' ','%20',req) 
    if(re.search('/$',req)):
      req=req[:-1]
    if(re.match('http://',req)):
      req=re.sub('http://',"https://",req)
    if(re.search('^#',req)):
      continue
    if re.search('^http(.*?)?.?uic.edu(.*?)',req):
      if(url.__contains__(req)):
        out.append(req)
        continue
      else:
        url.append(req)
        out.append(req)
    if re.search('^\/',req):
      
      try:
        base=re.match('https:\/\/(.*?)uic.edu',response.geturl()).group()
        if(url.__contains__(base+req)):
          out.append(req)
          continue
        else:
          url.append(base+req)
          out.append(req)
      except:

        logging.error("Navigational Error for %s",req)
        continue
  return url,out    



def crawler(START_URL,crawl_limit):
  logging.basicConfig(filename='crawler.log',level=logging.DEBUG,filemode='w')
  logging.info("Crawler Started")
  queue=[]
  visit=[]
  html_page=[]
  page_outlinks=[]
  queue.append(START_URL)
  print("Pages Crawled:..")
  while(len(queue)>0 and len(visit)<crawl_limit):
    outlinks=[]
    temp=[]
    req=queue.pop(0)
    logging.info("Page popped from queue %s",req)
    if(req in visit):
      continue
    else:
      if re.search('uic.edu',urlparse(req).hostname):
        html,res=read_page(req)
      if(res !=0):
        logging.debug("Page read %s %d",req,len(visit))
        html_page.append(html)
        visit.append(req)
        logging.info("%s added",req)
        temp,outlinks=(link_extraction_canonicalization(html,res))
        queue=queue+temp#(link_extraction_canonicalization(html,res))
        page_outlinks.append(outlinks)
        sys.stdout.write("\r%d" %  len(visit)+"/"+str(crawl_limit))
        sys.stdout.flush()
        #print(len(visit),"/",crawl_limit," ",req)
    logging.info("-------------------------------------------")
  crawled_pages=pd.DataFrame({"page_url":visit,"web_page":html_page,"outlink":page_outlinks})
  crawled_pages.to_pickle('./crawler.pk1')

start=time.time()
print("Web Crawler Started")

crawler(DATA_URL,6000)
print("Completed...")
print("File created...")
print(time.time()-start)






