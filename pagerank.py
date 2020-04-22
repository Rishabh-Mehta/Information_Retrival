import numpy as np
import pandas as pd
import pickle
import networkx as nx

def build_graph(df):
    web_graph = pd.DataFrame(columns=set(df['page_url']),index=set(df['page_url']))
    web_graph = web_graph.fillna(0)
    for i in range(len(df)):
        for j in range(len(df['outlink'][i])):
            web_graph[df['page_url'][i]][df['outlink'][i][j]] += 1
    return web_graph

# def initialize_page_rank(web_graph):
#     n=len(graph.index)
#     links=list(web_graph.index)
#     initial= [1/n]*n
#     S={links[i]:initial[i] for i in range(len(links))}
#     return S

# def adjacent_element(doc_list):
#     doc_list=list(doc_list.index[doc_list>0])
#     return doc_list

# def page_rank(web_graph,alpha,S):
#     n=len(web_graph)
#     links=list(web_graph.index)
#     initial= [1/n]*n
#     for i in range(len(web_graph)):
#       adj_j=[]
#       sum=0
#       adj_j=adjacent_element(web_graph.loc[links[i]])
#       for word in adj_j:
#         adj_k=[]
#         adj_k=adjacent_element(web_graph.loc[word])
#         denominator=1
#         for k in adj_k:
#           denominator+=web_graph[word][k]
#         sum+=alpha*(web_graph[links[i]][word]/denominator)*S[word] + ((1-alpha)*(1/n))
#       if sum!=0 and np.logical_not(np.isnan(sum)):
#         S[links[i]]=sum      
#     return S

data = pd.read_pickle('crawler.pk1')

print("Restricting page outlinks to scraped sites..")
data['outlink']= data['outlink'].apply(lambda x: [link for link in x if link in list(data['page_url'])])



print("Building Web Graph..")
graph = build_graph(data)



# print("Initializing Page rank..")
# rank = initialize_page_rank(graph)



# start = time.time()
# print("Calculating Page rank..")
# old = rank.copy()
# j=0
# update=page_rank(graph,0.85,rank)
# print("Running Page rank convergence..")
# while(update!=old and j<9):
#     j=j+1
#     print("iteration ",j,"..")
#     old=update.copy()
#     update=page_rank(graph,0.85,update)
# rank_f = update
# print(time.time() - start)




#Running page rank from networkx to avoid longer running time for page rank to converge 

print("Calculating Page rank..")
graph_np = graph.to_numpy()
nxgraph=nx.from_numpy_matrix(graph_np)
rank=nx.pagerank(nxgraph)
ind = list(graph.index)
page_rank = {k:v for k,v in zip(ind,list(rank.values()))}
pickle.dump(page_rank,open("./page_rank","wb"))