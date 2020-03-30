import numpy as np
import pandas as pd
import urllib
import re
import sys
from bs4 import BeautifulSoup
from html.parser import HTMLParser

def preprocess_tokenize(text):
    soup = BeautifulSoup(text,'html.parser')
    text = soup.prettify()
    text = re.sub('<!--.*-->','',text)
    text = re.sub('<[^>]*>','',text)
    text=re.sub('[^0-9a-zA-Z]',' ',text)
    text=re.sub(r"\b[nbrt]\b",' ',text)
    text = re.sub("\s+",' ',text)
    return text.split()


data = pd.read_pickle('crawler.pk1')
data['web_page']=data['web_page'].apply(lambda x:preprocess_tokenize(x))