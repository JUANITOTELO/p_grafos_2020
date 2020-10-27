import cell1, cell2, cell3
g = cell2.song_to_dict()

g2D = cell2.m_graph(g[1]+g[2], g[3])

cell3.GrafoSimple().crear_multigrafo(g,g2D)