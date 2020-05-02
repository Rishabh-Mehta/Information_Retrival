import numpy as np
import pandas as pd
import re
import pickle
import scipy.sparse
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import html
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup


lemma = WordNetLemmatizer()

def html_preprocessing(text):
    soup = BeautifulSoup(text)
    for script in soup(["script","style"]): 
        script.extract()
    text = soup.get_text()
    return text

def preprocess(text):
    #=re.sub("<script[^>]*>(.*?)<\/?script>"," ",str(text))
    #text = re.sub('<[^>]*>',' ',text)
    text = html_preprocessing(text)
    text=re.sub('[^a-zA-Z0-9-]',' ',text)
    text=re.sub(r"\b[nbrt]\b",' ',text)
    text = ' '.join([lemma.lemmatize(word) for word in text.split()])
    return text
data = pd.read_pickle('crawler.pk1')
data['web_page'] = data['web_page'].apply(lambda x:x.decode('latin-1'))
data.web_page = data.page_url + data.web_page
print("Preprocessing...")
data['cleaned']=data['web_page'].apply(lambda x:preprocess(x))
vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'),sublinear_tf=True,strip_accents='unicode')
print("Vectorizing..")
data_vector = vectorizer.fit_transform(pd.Series(data['cleaned']))
pickle.dump(vectorizer,open("./vectorizer","wb"))
scipy.sparse.save_npz('data_vector.npz',data_vector)

