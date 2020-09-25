"""
==============
Directed Graph
==============

Draw a graph with directed edges using a colormap and different node sizes.

Edges have different colors and alphas (opacity). Drawn using matplotlib.
"""

import netgraph
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy
import main

n = main.notas
G = nx.DiGraph()
for i in range(len(n)):
    if i != 0:
        G.add_edge(n[i-1],n[i])

pos = nx.layout.kamada_kawai_layout(G)

d = dict(G.degree)
low, *_, high = sorted(d.values())
norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
node_sizes = [v*10 for v in d.values()]
M = G.number_of_edges()
edge_colors = range(2,M+2)
edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
fig = plt.figure()
nodes = nx.draw_networkx_nodes(
    G, 
    pos, 
    node_size=node_sizes, 
    node_color=[mapper.to_rgba(i) for i in d.values()]
    )
edges = nx.draw_networkx_edges(
    G,
    pos,
    node_size=node_sizes,
    arrowstyle="wedge",
    arrowsize=10,
    edge_color=edge_colors,
    edge_cmap=plt.cm.Blues,
    width=2,
)
labels = nx.draw_networkx_labels(
    G,
    pos,
    font_size=10,
    font_color="white",
)
# set alpha value for each edge
for i in range(M):
    edges[i].set_alpha(edge_alphas[i])

# pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
# pc.set_array(edge_colors)
# plt.colorbar(pc)

ax = plt.gca()
ax.set_axis_off()
fig.set_facecolor("#9e9998")
fig.set_size_inches((15,15))
fig.savefig("g1.png")
#plt.show()
