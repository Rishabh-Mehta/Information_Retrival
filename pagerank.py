import numpy as np
import pandas as pd
import re
import pickle
import scipy.sparse
import sys
import time
import urllib.request
import urllib.error


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
        
        continue
      else:
        url.append(req)
    if re.search('^\/',req):
      
      try:
        base=re.match('https:\/\/(.*?)uic.edu',response.geturl()).group()
        if(url.__contains__(base+req)):
          
          continue
        else:
          url.append(base+req)
      except:

        logging.error("Navigational Error for %s",req)
        continue
  return url





data = pd.read_pickle('crawler.pk1')

web_graph = pd.DataFrame(columns=set(data['page_url']),index=set(data['page_url']))
web_graph = web_graph.fillna(0)
