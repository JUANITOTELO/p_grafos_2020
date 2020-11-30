import cell1, cell2, cell3, BA, FW
import moviepy.editor as mp
import networkx as nx
import os
import matplotlib.pyplot as plt

try:
    g = cell2.song_to_dict()
    g2D = cell2.m_graph(g[1]+g[2], g[3])
    #cell1.c_3D(g2D[0],g2D[1])
    #a = BA.BusquedaProfundidad()
    #ae = a.arbol_de_expan(g, g2D)
    #FW.centro_FW(g2D[0],g2D[1])
except:
    pass
