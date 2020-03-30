import numpy as np
import pandas as pd
import urllib.request
import urllib.error
import re
import sys
import time

DATA_URL = 'https://cs.uic.edu'

def read_page(req):
    try:
        if(re.search('/$',req)):
            req=req[:-1]
        response = urllib.request.urlopen(req)
        content = response.getheader('Content-Type')
        #print("Visited",req)
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
  links=re.finditer("<a.*?href=\"(.*?)\".*?<\/?a>",str(page))
  for link in links:
    req=link.group(1)
    req=re.sub(' ','%20',req) 
    if(re.search('/$',req)):
      req=req[:-1]
    elif(re.match('http://',req)):
      req=re.sub('http://',"https://",req)
    elif(re.search('^#',req)):
      continue
    elif re.search('^http(.*?).uic.edu(.*?)',req):
      if(url.__contains__(req)):
        continue
      else:
        #print(link.group(1))
        url.append(link.group(1))
    elif re.search('^/',link.group(1)):
      req=re.match('https:\/\/(.*?)uic.edu',response.geturl()).group()
      if(url.__contains__(req+link.group(1))):
        continue
      else:
        url.append(req+link.group(1))
        #print(req+link.group(1))
  return url    

def clean_page(text):
    text=re.sub("<head>(.*?)<\/?head>"," ",str(text))
    text=re.sub("<script>(.*?)<\/?script>"," ",str(text))
    return text

def crawler(START_URL,crawl_limit):
  queue=[]
  visit=[]
  html_page=[]
  queue.append(START_URL)
  print("Pages Crawled:..")
  while(len(queue)>0 and len(visit)<crawl_limit):
    req=queue.pop(0)
    if(req in visit):
      #print("Already checked")
      continue
    else:
      html,res=read_page(req)
      if(res !=0):
        html=clean_page(html)
        html_page.append(html)
        visit.append(req)
        queue=queue+(link_extraction_canonicalization(html,res))
        time.sleep(1)
        sys.stdout.write("\r%d" %  len(visit)+"/"+str(crawl_limit))
        sys.stdout.flush()
  crawled_pages=pd.DataFrame({"page_url":visit,"web_page":html_page})
  crawled_pages.to_pickle('./crawler.pk1')
start=time.time()
print("Web Crawler Started")

crawler(DATA_URL,3500)
print("Completed...")
print("File created...")
print(time.time()-start)




# re.sub("(\\b<(.*?)>\\b)"," ",str(html))
