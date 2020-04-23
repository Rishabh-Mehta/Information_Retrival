import numpy as np
import pandas as pd
import re
import pickle
import scipy.sparse
import sys
import time
from nltk.corpus import stopwords
np.seterr(divide='ignore', invalid='ignore')
np.set_printoptions(threshold=sys.maxsize)

start = time.time()
data_vector = scipy.sparse.load_npz('data_vector.npz')
vectorizer = pickle.load(open('vectorizer','rb'))
page_rank = pickle.load(open('page_rank','rb'))
data = pd.read_pickle('crawler.pk1')
#query = sys.argv[1]
query="oncampus job"

def retrive(q):
    q =q.lower()
    q=' '.join(w for w in q.split() if not w in stopwords.words('english'))
    q=vectorizer.transform([q])
    retrival = []
    for i in range(data_vector.shape[0]):
        if(np.any(np.logical_and(q.toarray(),data_vector[i].toarray()))):
        
            match = set(q.nonzero()[1]) & set(data_vector[i].nonzero()[1]) 
            mismatch = set(q.nonzero()[1]) - set(data_vector[i].nonzero()[1])
            sim = (data_vector[i].dot(q.T)).toarray()/ scipy.sparse.linalg.norm(data_vector[i]) + page_rank[data.page_url[i]]
            retrival.append([data.page_url[i],sim,match,mismatch])        
    if retrival == []:
        print("Query does not match any documents")
        sys.exit()
    retrival.sort(key=lambda x:x[1],reverse=True)
    return retrival

def matched_words(Result,k):
    for R in Result:
        match =list(R[k])
        for i in range(len(match)):
            match[i] = vectorizer.get_feature_names()[match[i]]
        R[k] = match
    return Result

result = retrive(query)
result = matched_words(result,2)
result = matched_words(result,3)

result = pd.DataFrame(result,columns=["URL","Similarity","Matched Words","Unmatched Words"])
print(result)
print(time.time()-start)


