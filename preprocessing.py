import numpy as np
import pandas as pd
import urllib
import re
import sys
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess(text):
    soup = BeautifulSoup(text,'html.parser')
    text = soup.prettify()
    text = re.sub('<!--.*-->','',text)
    text = re.sub('<[^>]*>','',text)
    text=re.sub('[^0-9a-zA-Z]',' ',text)
    text=re.sub(r"\b[nbrt]\b",' ',text)
    text = re.sub("\s+",' ',text)
    return text



data = pd.read_pickle('crawler.pk1')
data['web_page']=data['web_page'].apply(lambda x:preprocess(x))


tfidf = TfidfVectorizer()
tfidf.fit_transform(data['web_page'])