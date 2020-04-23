import numpy as np
import pandas as pd
import re
import pickle
import scipy.sparse
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


def preprocess_tokenize(text):
    text=str(text)
    text=re.sub("<script[^>]*>(.*?)<\/?script>"," ",str(text))
    text = re.sub('<[^>]*>',' ',text)
    text=re.sub('[^a-zA-Z0-9.-]',' ',text)
    text=re.sub(r"\b[nbrt]\b",' ',text)
    return text

data = pd.read_pickle('crawler.pk1')
data['cleaned']=data['web_page'].apply(lambda x:preprocess_tokenize(x))
vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'),sublinear_tf=True)
data_vector = vectorizer.fit_transform(pd.Series(data['cleaned']))
pickle.dump(vectorizer,open("./vectorizer","wb"))
scipy.sparse.save_npz('data_vector.npz',data_vector)

