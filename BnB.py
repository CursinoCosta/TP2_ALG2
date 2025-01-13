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
  n_nos = G.number_of_nodes()
  escolhidos = caminho[:-1]
  resto = list(range(1,n_nos+1))
  resto = [x for x in resto if x not in caminho]
  ultimo = caminho[-1]
  falta = [caminho[0]] + resto

  for i in range(len(caminho)-1):
    sum += G[caminho[i]][caminho[i+1]]['weight']
  if(resto):
    sum += min([G[ultimo][i]['weight'] for i in resto])
  else:
    sum += G[ultimo][caminho[0]]['weight']

  for v in resto:
    sum += min([G[v][i]['weight'] for i in filter(lambda x: x != v, falta)])

  return sum



def BnB(G, n, r):
  best_bound = bound(G,list(G.nodes())) #cria um bound inicial do caminho 0,1,2,3,...,n
  raiz = (0,bound(G,[r]),0,[r]) # (nivel,bound,custo,caminho)
  sol = list(G.nodes())
  queue = [raiz]
  hq.heapify(queue)
  while(queue):
    no = hq.heappop(queue)
    #print(len(queue),best_bound,no)
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
          new_bound = bound(G,no[3]+[k])        
          pesoNoK = G[no[3][-1]][k]['weight']
          if(not isin and pesoNoK != np.inf and new_bound < best_bound):
            hq.heappush(queue,(no[0]-1,new_bound,no[2]+pesoNoK,no[3]+[k]))
            #queue.insert(0,(new_bound,no[2]+pesoNoK,no[0]+1,no[3]+[k]))
      elif(G[no[3][-1]][r]['weight'] != np.inf and len(no[3]) == G.number_of_nodes() and no[1] < best_bound):
        #print('add')
        hq.heappush(queue,(no[0]-1,no[1],no[2]+G[no[3][-1]][r]['weight'],no[3]+[0]))
        #queue.insert(0,(no[1],no[2]+G[no[3][-1]][r]['weight'],no[0]+1,no[3]+[0]))
  return sol,best_bound
            
  