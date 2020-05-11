#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taller 2

Ruta de minimo costos entre dos nodos aleatorios con dijkstra.

Sebastian Garcia 201630047
Nicolas Sotelo 201623026
"""

from collections import defaultdict
from random import seed
from random import randint
import matplotlib.pyplot as plt
import math

plt.style.use('ggplot')

# ==============
# GRAPH
# ==============

class Graph():
    def __init__(self):
        """
        self.edges ws un dict con los posibles nodos alcanzables apartir de uno
        e.g. {'X': ['A', 'B', 'C'], ...}
        self.cost distancia entre dos nodos, tupla -> costo
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.cost = {}
    
    def add_edge(self, from_node, to_node, weight):
        # se asume grafo bi direccional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.cost[(from_node, to_node)] = weight
        self.cost[(to_node, from_node)] = weight
        
        
# ==============
# DIJKSTRA
# ==============
        
        
def dijsktra(graph, initial, end):
    # el camino mas corto es un dict de nodos
    # con valor = (nodo anteriro, costo)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.cost[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "RUTA NO POSIBLE"
        # se escoje camino con menor costo (distancia)
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # registro del camino
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # rever para obtener el orden inicio -> fin
    path = path[::-1]
    return path



# ==============
# SETS
# ==============
    

# cantidad de nodos
num_nodes = 100


# radio de comunicacion 
RC = 14 


# coordenadas
coorX = []
coorY = []


seed(1)
for _ in range(num_nodes):
	coorX.append(randint(0, num_nodes))
	coorY.append(randint(0, num_nodes))
         
   

# representacion del grafo
graph = Graph()
edges = []
nodes = {}



# ==============
# PLOT NODOS INICIALES
# ==============
fig1 = plt.figure(1)
for cont in range(len(coorX)):
    x = coorX[cont]
    y = coorY[cont]
    lbl = str(cont+1)

    plt.plot(x, y, 'rx')
    plt.text(x - 2, y + 1, lbl, rotation=0, size=8, weight='bold')
    nodes[lbl] = f"{x},{y}"
# end

         
# ==============
# PLOT CAMINOS POSIBLES
# ==============              
for node in nodes:
    xi = int(nodes[node].split(",")[0])
    yi = int(nodes[node].split(",")[1])
    for _node in nodes:
        if node != _node:
          xf = int(nodes[_node].split(",")[0])
          yf = int(nodes[_node].split(",")[1] )
          
          x = xi - xf
          y = yi - yf
          distancia = math.sqrt( pow(x, 2) + pow(y, 2 ))
          if distancia <= RC:
              # registro de distancia entre nodos
              edges.append(( node, _node, distancia ))
              plt.plot([xi, xf], [yi, yf], 'w--')
          
# end
                
           
# registro nodos y sus distancias en el grafo
for edge in edges:
    graph.add_edge(*edge)


# random nodo origen y destino
seed(4)
nodo_origen = randint(0, num_nodes) 
nodo_destino = randint(0, num_nodes)

while nodo_origen == nodo_destino:
    nodo_origen = randint(0, num_nodes) 


# camino Dijkstra :: 
# Mirar la gráfica resultante para tener certeza de los nodos que estan conectados 
path = dijsktra(graph, str(nodo_origen), str(nodo_destino))


print(f'''\n
-------------------------
      RESULTADOS
-------------------------\n

Nodo Origen:    {nodo_origen}
Nodo Destino:   {nodo_destino}

Camino:         {path}

      ''')


# ==============
# PLOT CAMINO DIJKSTRA
# ==============
if path != "RUTA NO POSIBLE":
    for i in range(0, len(path) - 1):
        xi = int(nodes[path[i]].split(",")[0])
        yi = int(nodes[path[i]].split(",")[1])
        
        xf = int(nodes[path[i+1]].split(",")[0])
        yf = int(nodes[path[i+1]].split(",")[1])
        
        plt.plot([xi, xf], [yi, yf], 'b-')


