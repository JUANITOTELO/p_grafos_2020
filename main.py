import cell1, cell2, cell3, BA, FW
import networkx as nx
import matplotlib.pyplot as plt

g = cell2.song_to_dict()
g2D = cell2.m_graph(g[1]+g[2], g[3])

# a = BA.BusquedaProfundidad()
# a.arbol_de_expan()

FW.centro_FW(g2D[0],g2D[1])