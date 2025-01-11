#Implementação do Twice Around the Tree
import networkx as nx

def Weight(caminho):
  W = 0
  for i in range(len(caminho)-1):
    # print(f'{caminho[i]}-{caminho[i+1]}')
    W += G[caminho[i]][caminho[i+1]]['weight']
  return W

def TatT(G, r):
    T = nx.minimum_spanning_tree(G,algorithm='prim')
    H = list(nx.dfs_preorder_nodes(T, source=r))
    H.append(H[0])

    W = Weight(H)
    
    return H, W
