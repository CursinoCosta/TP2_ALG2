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

def bound(G,caminho = [],r=1): #retorna bound*-1 para uso de min heap
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
          sum += (t[mins[0]] + G[r][caminho[1]]['weight'])
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



def BnB(G, n, r):
  best_bound = bound(G,list(G.nodes()),r) #cria um bound inicial do caminho 0,1,2,3,...,n
  raiz = (0,bound(G),0,[r]) # (nivel,bound,custo,caminho)
  sol = list(G.nodes())
  queue = [raiz]
  hq.heapify(queue)
  while(queue):
    no = hq.heappop(queue)
    #print(len(queue),no)
    #no = queue.pop()
    if(np.isin(4,no[3]) and not np.isin(3,no[3])): continue
    if(no[0] < -(n-1)):
      if(best_bound > no[2]):
        #print('busca')
        best_bound = no[2]
        #print('newbest ',best_bound)
        sol = no[3]
    elif(no[1] < best_bound):
      if(no[0] > -(n-1)):
        for k in range(1,n+1):
          isin = np.isin(k,no[3])
          if(isin): continue
          new_bound = bound(G,no[3]+[k],r)        
          pesoNoK = G[no[3][-1]][k]['weight']
          if(not isin and pesoNoK != np.inf and new_bound < best_bound):
            hq.heappush(queue,(no[0]-1,new_bound,no[2]+pesoNoK,no[3]+[k]))
            #queue.insert(0,(new_bound,no[2]+pesoNoK,no[0]+1,no[3]+[k]))
      elif(G[no[3][-1]][r]['weight'] != np.inf and len(no[3]) == G.number_of_nodes() and no[1] < best_bound):
        #print('add')
        hq.heappush(queue,(no[0]-1,no[1],no[2]+G[no[3][-1]][r]['weight'],no[3]+[0]))
        #queue.insert(0,(no[1],no[2]+G[no[3][-1]][r]['weight'],no[0]+1,no[3]+[0]))
  return sol,best_bound
            
  