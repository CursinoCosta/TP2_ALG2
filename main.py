import math
import networkx as nx

def Graph(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    nodes = []
    
    for line in lines:
        line = line.strip()

        if line == "DIMENSION":
            parts = line.split()
            size = parts[1]
            continue

        if line == "NODE_COORD_SECTION":
            parts = line.split()
            node_id = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            nodes.append((node_id, x, y))
            continue
        
        if line == "EOF":
            break
        
        
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
    
    return G

