import networkx as nx
import netgraph
import math
import matplotlib.colors as mc
import matplotlib.pyplot as plt
import numpy as np
import main

n = main.notas
n = n[::-1]
G = nx.DiGraph()
for i in range(len(n)):
    n[i-1] = n[i-1].replace('4', '')
    n[i] = n[i].replace('4', '')
    if i != 0:
        G.add_edge(n[i-1], n[i])
print(n)
pos = nx.layout.shell_layout(G, rotate= -(np.pi+(np.pi/3)))
nodesColors = []
for i in G.nodes:
    if("#" in i):
        nodesColors.append((0.0,0.0,0.0))
    else:
        nodesColors.append((1.0,1.0,1.0))
semitonos = []
for i in range(len(list(G.edges))):
    semitonos.append("1/2")
semitonos = dict(zip(G.edges,semitonos))
fig = plt.figure()
nx.draw_networkx_nodes(
    G,
    pos,
    node_size=800,
    node_color=nodesColors
)
nx.draw_networkx_edges(
    G,
    pos,
    node_size=800,
    arrowstyle="<-",
    arrowsize=10,
    width=2,
    connectionstyle="arc3,rad=0.2",
    
)
nx.draw_networkx_edge_labels(G,pos,edge_labels=semitonos,rotate=False)
nx.draw_networkx_labels(
    G,
    pos,
    font_size=12,
    font_color="orange",
)


ax = plt.gca()
ax.set_axis_off()
fig.set_size_inches((7, 7))
fig.set_facecolor("#564f4f")
plt.savefig('Escalas/Grafo_{0}.png'.format(main.nombre))
plt.show()
