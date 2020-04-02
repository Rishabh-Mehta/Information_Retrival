import numpy as np
import pandas as pd
import re
import pickle
import scipy.sparse
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
    return text


data = pd.read_pickle('crawler.pk1')
data['tokens']=data['web_page'].apply(lambda x:preprocess_tokenize(x))
vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
data_vector = vectorizer.fit_transform(pd.Series(data['tokens']))
pickle.dump(vectorizer,open("./vectorizer","wb"))
scipy.sparse.save_npz('data_vector.npz',data_vector)