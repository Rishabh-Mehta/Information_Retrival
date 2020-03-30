import numpy as np
import pandas as pd
import urllib
import re
import sys
from bs4 import BeautifulSoup
from html.parser import HTMLParser


myhtml = HTMLParser()

data = pd.read_pickle("crawler.pk1")
data.to_csv('web.csv')
soup = BeautifulSoup(data['web_page'][0],'html.parser')
print(soup.prettify())
re.sub("(\\b<(.*?)>\\b)"," ",str(html))

data['web_page'] = data['web_page'].apply(lambda x:re.sub("(\\b<(.*?)>\\b)"," ",str(x)))


def clean(text):
    soup = BeautifulSoup(text,'html.parser')
    text = soup.prettify()
    text = re.sub('<!--.*-->','',text)
    text = re.sub('<[^>]*>','',text)
    text=re.sub('[^0-9a-zA-Z]',' ',text)
    text=re.sub(r"\b[nbrt]\b",' ',text)
    text = re.sub("\s+",' ',text)
    return text

html = clean(data['web_page'][0])

