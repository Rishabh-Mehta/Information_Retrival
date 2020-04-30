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
query = sys.argv[1]


def retrive(q):
    q =q.lower()
    q=' '.join(w for w in q.split() if not w in stopwords.words('english'))
    q=vectorizer.transform([q])
    retrival = []
    for i in range(data_vector.shape[0]):
        if(np.any(np.logical_and(q.toarray(),data_vector[i].toarray()))):
            match = set(q.nonzero()[1]) & set(data_vector[i].nonzero()[1]) 
            mismatch = set(q.nonzero()[1]) - set(data_vector[i].nonzero()[1])
            sim=(data_vector[i].dot(q.T)).toarray()/ scipy.sparse.linalg.norm(data_vector[i])
            pagerank=page_rank[data.page_url[i]]
            netscore = sim +pagerank
            retrival.append([data.page_url[i],netscore,match,mismatch,sim,pagerank,i])        
    if retrival == []:
        print("Query does not match any documents")
        sys.exit()
    retrival.sort(key=lambda x:x[1],reverse=True)
    query_expansion = pseudo_relevance(retrival,10,q)
    return retrival[0:20],query_expansion

def pseudo_relevance(result,k,q):
    result.sort(key=lambda x:x[4],reverse=True)
    result = result[:k]
    rel_index=[item[6] for item in result]
    relevant_vector=np.zeros(data_vector.shape[1])
    non_relevant_vector=(scipy.sparse.csr_matrix.sum(data_vector.T,axis=1)).T
    for i in rel_index:
        relevant_vector +=data_vector[i]
    relevant_vector = 0.75*(relevant_vector / k)
    non_relevant_vector -=relevant_vector
    non_relevant_vector = 0.15*(non_relevant_vector / (data_vector.shape[0]-k))
    q_new = q + relevant_vector + non_relevant_vector
    q_opt = (np.argsort(-q_new)).T[:5]
    query_exp = query_expansion(q_opt)
    return query_exp
     

def matched_words(Result,k):
    for R in Result:
        match =list(R[k])
        for i in range(len(match)):
            match[i] = vectorizer.get_feature_names()[match[i]]
        R[k] = match
    return Result
def query_expansion(q):
    query=''
    for i in list(q):
        query += ' '+vectorizer.get_feature_names()[int(i)]
    return query 

    
result,new_query = retrive(query)
result = matched_words(result,2)
result = matched_words(result,3)

result = pd.DataFrame(result,columns=["URL","Net Score","Matched Words","Unmatched Words","Similarity","Page Rank","Doc Id"])
print("Query Expansion ",new_query)
print(result)
print(time.time()-start)


