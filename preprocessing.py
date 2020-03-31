import numpy as np
import pandas as pd
import urllib
import re
import sys
from bs4 import BeautifulSoup
import nltk
nltk.download('popular')
from nltk.corpus import stopwords

def preprocess_tokenize(text):
    soup = BeautifulSoup(text,'html.parser')
    text = soup.prettify()
    text = re.sub('<!--.*-->','',text)
    text = re.sub('<[^>]*>','',text)
    text=re.sub('[^0-9a-zA-Z]',' ',text)
    text=re.sub(r"\b[nbrt]\b",' ',text)
    text = re.sub(r"\s+",' ',text)
    text=text.lower()
    text = ' '.join(word for word in text.split() if word not in stopwords.words('english'))
    return text.split()

def generate_inverted_index(df):
    inv = {}
    for i in range(len(df)):
        for word in set(df.tokens[i]):
            if word not in inv.keys():
                inv[word] = [[df.index[i],pd.Series(df.tokens[i]).value_counts()[word]]]
            elif word in inv.keys():
                inv[word].append([df.index[i],pd.Series(df.tokens[i]).value_counts()[word]])
    return inv



import time 
start = time.time()
print("Pre processing..")
data = pd.read_pickle('crawler.pk1')
data['tokens']=data['web_page'].apply(lambda x:preprocess_tokenize(x))
print(time.time()-start)
start =time.time()
print("inverted index")
inverted_index = generate_inverted_index(data)
print(time.time()-start)