#Implementação do Twice Around the Tree
import networkx as nx

def TatT(G, c):
    MST = nx.minimum_spanning_tree(G,algorithm='prim')
    