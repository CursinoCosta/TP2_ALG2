#Implementação do Twice Around the Tree
import networkx as nx

def TatT(G, c):
    T = nx.minimum_spanning_tree(G, algorithm='prim')
    return list(nx.dfs_preorder_nodes(T, source=0))
    