import numpy as np
import pandas as pd
import re
import pickle
import scipy.sparse
import sys
import time
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
np.seterr(divide='ignore', invalid='ignore')
np.set_printoptions(threshold=sys.maxsize)

data_vector = scipy.sparse.load_npz('data_vector.npz')
vectorizer = pickle.load(open('vectorizer','rb'))
page_rank = pickle.load(open('page_rank','rb'))
data = pd.read_pickle('crawler.pk1')




