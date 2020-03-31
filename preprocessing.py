import numpy as np
import pandas as pd
import urllib
import re
import sys
from bs4 import BeautifulSoup
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_tokenize(text):
    soup = BeautifulSoup(text,'html.parser')
    text = soup.prettify()
    text = re.sub('<!--.*-->','',text)
    text = re.sub('<[^>]*>','',text)
    text=re.sub('[^a-zA-Z]',' ',text)
    text=re.sub(r"\b[nbrt]\b",' ',text)
    #text = re.sub(r"\s+",' ',text)
    text=text.lower()
    return text

# def generate_inverted_index(df):
#     inv = {}
#     for i in range(len(df)):
#         for word in set(df.tokens[i]):
#             if word not in stopwords.words('english'):
#                 if word not in inv.keys():
#                     inv[word] = [[df.index[i],pd.Series(df.tokens[i]).value_counts()[word]]]
#                 elif word in inv.keys():
#                     inv[word].append([df.index[i],pd.Series(df.tokens[i]).value_counts()[word]])
#     return inv




print("Pre processing..")
data = pd.read_pickle('crawler.pk1')
data['tokens']=data['web_page'].apply(lambda x:preprocess_tokenize(x))

# print("inverted index")
# inverted_index = generate_inverted_index(data)

vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
data_vector = vectorizer.fit_transform(pd.Series(data['tokens']))