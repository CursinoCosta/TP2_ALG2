#Implementação do algoritmo de Christofides
import networkx as nx
import heapq as hq
import numpy as np
import matplotlib.pyplot as plt


#funçoes auxiliares

def plota_grafo(G):
  pos = nx.spring_layout(G)  # Layout para distribuir os nós de forma legível
  nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10, font_weight='bold')

    # Desenha os pesos nas arestas
  edge_labels = nx.get_edge_attributes(G, 'weight')
  nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Exibe o grafo
  plt.show()

def dfs(G, u, visited=None):
  result = []
  if visited is None:
    visited = set()
  visited.add(u)

  for v in G.neighbors(u):
    if v not in visited:
      #print(f'{u}-{v}')
      result.append([u, v])
      result.extend(dfs(G, v, visited))

  return result

def Weight(caminho):
  W = 0
  for i in range(len(caminho)-1):
    # print(f'{caminho[i]}-{caminho[i+1]}')
    W += G[caminho[i]][caminho[i+1]]['weight']
  return W

def Christofides(G, r):
  T = nx.minimum_spanning_tree(G, algorithm='prim')
  g = nx.MultiGraph(T)
  grau_impar = []
  # print('arvore geradora')
  # plota_grafo(T)


  for v in T.nodes:
    # print(f'vertice {v} grau {T.degree[v]}')
    if T.degree[v]%2 != 0:
      grau_impar.append(v)

  M = nx.algorithms.min_weight_matching(G.subgraph(grau_impar), weight='weight')

  # print(f'matching{M}')

  g.add_edges_from(M)

  # plota_grafo(g)

  circuito_euleriano = dfs(g, r)

  # print(circuito_euleriano)

  caminho = []
  visited = set()
  for u, v in circuito_euleriano:
      if u not in visited:
          caminho.append(u)
          visited.add(u)
      if v not in visited:
          caminho.append(v)
          visited.add(v)
  caminho.append(caminho[0])

  W = Weight(caminho)

  return caminho, W

