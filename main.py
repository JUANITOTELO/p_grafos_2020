import cell1, cell2, cell3, BA
import networkx as nx
import matplotlib.pyplot as plt

#g = cell2.song_to_dict()
#g2D = cell2.m_graph(g[1]+g[2], g[3])

bea = BA.BusquedaProfundidad()
e_eT = []
visitados = set()
g = cell2.song_to_dict()
g2D = cell2.m_graph(g[1]+g[2], g[3])
eT = bea.tG(g2D[0])
v_T = list(eT.keys())
t2D = nx.Graph()
bea.dfs(visitados, eT, v_T[0],e_eT)
t2D.add_edges_from(e_eT)
cell3.GrafoSimple().crear_multigrafo((t2D, "Árbol-Exp-{0}".format(g2D[1])))