import cell1, cell2, cell3
import networkx as nx
import matplotlib as mpl
from progressbar import progressbar
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

class BusquedaProfundidad:
    """
    Clase para el algoritmo de profundidad
    """
    def tG(self, G):
        """Recibe un grafo G y retorna un diccionario de adyacencia."""
        v_G = list(G.nodes)
        e_G = list(G.edges)
        T = dict(zip(v_G, [[] for i in range(len(v_G))]))
        for i in progressbar(v_G):
            for j in e_G:
                if i == j[0]:
                    T[i].append(j[1])
            time.sleep(0.02)
        #print(T)
        return T
        

    def dfs(self, visitados, graph, node, e_eT):
        if node not in visitados:
            print (node)
            visitados.add(node)
            for neighbour in progressbar(graph[node]):
                if node != neighbour and neighbour not in visitados:
                    e_eT.append((node, neighbour))
                    self.dfs(visitados, graph, neighbour,e_eT)
                    time.sleep(0.02)

