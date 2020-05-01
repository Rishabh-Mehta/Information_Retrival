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

lemma = WordNetLemmatizer()

def preprocess_tokenize(text):
    text=html.unescape(str(text))
    text=re.sub("<script[^>]*>(.*?)<\/?script>"," ",str(text))
    text = re.sub('<[^>]*>',' ',text)
    text=re.sub('[^a-zA-Z0-9-]',' ',text)
    text=re.sub(r"\b[nbrt]\b",' ',text)
    text = ' '.join([lemma.lemmatize(word) for word in text.split()])
    return text
data = pd.read_pickle('crawler.pk1')
data['web_page'] = data['web_page'].apply(lambda x:x.decode('latin-1'))
data.web_page = data.page_url + data.web_page
# data['cleaned']=data['web_page'].apply(lambda x:preprocess_tokenize(x))
# vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'),sublinear_tf=True,strip_accents='unicode')
# data_vector = vectorizer.fit_transform(pd.Series(data['web_page']))
# pickle.dump(vectorizer,open("./vectorizer","wb"))
# scipy.sparse.save_npz('data_vector.npz',data_vector)
