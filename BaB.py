import networkx as nx
import heapq as hq
import numpy as np


#Implementação do Branch and Bound
def min_edges(t, n):
  auxt = t.copy()
  mins = []
  for i in range(n):
    min = np.argmin(auxt)
    auxt[min] = np.inf
    mins.append(min)
  return mins

def bound(G,caminho = []): #retorna bound*-1 para uso de min heap
  sum = 0
  #nao existe caminho ainda
  if(not caminho):
    for no in G.nodes():
      edges = list(G.edges(no,data=True))
      t = [list(t[2].values())[0] for t in edges]
      mins = min_edges(t,2)
      sum += (t[mins[0]]+t[mins[1]])
    return sum/2
  #existe um caminho completo
  if(len(caminho) == len(G.nodes())):
    sum = 0
    for i in range(len(caminho)-1):
      sum += G[caminho[i]][caminho[i+1]]['weight']
    sum += G[caminho[-1]][caminho[0]]['weight']
    return sum
  #existe um caminho incompleto
  else:
    sum = 0
    counter = 0
    for v in caminho:
      edges = list(G.edges(v,data=True))
      t = [list(t[2].values())[0] for t in edges]
      mins = min_edges(t,2)
      if(counter == 0):
        if(edges[mins[0]][1] == caminho[1]):
          sum += (t[mins[0]]+t[mins[1]])
        else:
          sum += (t[mins[0]] + G[0][caminho[1]]['weight'])
      elif(counter == len(caminho)-1):
        if(edges[mins[0]][1] == caminho[-2]):
          sum += (t[mins[0]]+t[mins[1]])
        else:
          sum += (t[mins[0]] + G[caminho[-2]][v]['weight'])
      else:
        sum += (G[v][caminho[counter + 1]]['weight'] + G[v][caminho[counter-1]]['weight'])
      counter += 1
    for v in G.nodes():
      if(np.isin(v,caminho)): continue
      edges = list(G.edges(v,data=True))
      t = [list(t[2].values())[0] for t in edges]
      mins = min_edges(t,2)
      sum += (t[mins[0]]+t[mins[1]])
          
    return sum/2


def BnB(G, n):
  best_bound = bound(G,list(G.nodes())) #cria um bound inicial do caminho 0,1,2,3,...,n
  raiz = (bound(G),0,0,[0]) # (bound,custo,nivel,caminho)
  sol = list(G.nodes())
  queue = [raiz]
  hq.heapify(queue)
  while(queue):
    no = hq.heappop(queue)
    if(no[2] > n-1):
      if(best_bound > no[1]):
        best_bound = no[1]
        sol = no[3]
    elif(no[0] < best_bound):
      if(no[2] < n-1):
        for k in range(1,n):
          isin = np.isin(k,no[3])
          if(isin): continue
          new_bound = bound(G,no[3]+[k])        
          pesoNoK = G[no[3][-1]][k]['weight']
          if(not isin and pesoNoK != np.inf and new_bound < best_bound):
            hq.heappush(queue,(new_bound,no[1]+pesoNoK,no[2]+1,no[3]+[k]))
      elif(G[no[3][-1]][0]['weight'] != np.inf and len(no[3]) == G.number_of_nodes() and no[0] < best_bound):
        hq.heappush(queue,(no[0],no[1]+G[no[3][-1]][0]['weight'],no[2]+1,no[3]+[0]))
  return sol,best_bound
        
            
  