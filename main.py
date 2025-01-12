import math
import networkx as nx
import Christofides
import TAtT
import BnB
import time

def Graph(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    nodes = []
    nodeinfo = False
    for line in lines:
        line = line.strip()
        parts = line.split()
        

        if parts[0] == "NAME":
            name = parts[2]  
            continue

        if parts[0] == "NAME:":
            name = parts[1]  
            continue

        if parts[0] == "DIMENSION":
            size = int(parts[2])
            continue

        if parts[0] == "DIMENSION:":
            size = int(parts[1])
            continue

        if parts[0] == "NODE_COORD_SECTION":
            nodeinfo = True
            continue

        if parts[0] == "EOF":
            break
        
        if nodeinfo:
            node_id = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            nodes.append((node_id, x, y))
        
    G = nx.Graph()
    
    for node_id, x, y in nodes:
        G.add_node(node_id, pos=(x, y))
    
    # Adicionar arestas com pesos euclidianos
    for i in range (size):
        for j in range(i + 1, size):
            id1, x1, y1 = nodes[i]
            id2, x2, y2 = nodes[j]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            G.add_edge(id1, id2, weight=distance)
    
    return G , size, name

(G,size,name) = Graph('ALL_tsp/d493.tsp')
#init = time.time()
#bnb = BnB.BnB(G,size,1)
#t_bnb = time.time()
tatt = TAtT.TatT(G,1)
print(tatt)
#t_tatt = time.time()
#Chris = Christofides.Christofides(G,1)
#t_Chris = time.time()

#print(bnb[1],' time bnb :',t_bnb,'\n',tatt[1],' time tatt :',t_tatt,'\n',Chris[1],' time Chris :',t_Chris,'\n')
