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
    (old_lvl, old_bound, old_cost, old_path) = hq.heappop(queue)

    if(np.isin(4,old_path) and not np.isin(3,old_path)): continue

    if(old_bound < best_bound):
      new_lvl = old_lvl - 1
      for i in filter(lambda x: x not in old_path,list(range(1,n+1))):
        new_path = old_path.copy() + [i]
        new_cost = old_cost + G[old_path[-1]][i]['weight']

        if(new_lvl == -(n-1)):
          new_cost += G[i][1]['weight']
          if(best_bound > new_cost):
            best_bound = new_cost
            sol = new_path

        else:
          new_bound = bound(G,new_path)
          if(new_bound<best_bound):
            hq.heappush(queue,(new_lvl,new_bound,new_cost,new_path))
            
  return sol,best_bound
            
  