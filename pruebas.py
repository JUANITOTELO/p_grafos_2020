import networkx as nx
import netgraph
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy
import main
options = {
    'node_color': 'black',
    'font_color': 'orange',
    'node_size': 200,
    'width': 0.5
}
n = main.notas
G = nx.DiGraph()
for i in range(len(n)):
    if i != 0:
        G.add_edge(n[i-1],n[i])
print(G.nodes())
d = dict(G.degree)
low, *_, high = sorted(d.values())
norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
nx.draw_kamada_kawai(G, 
        nodelist=d,
        node_size=100,
        
        node_color=[mapper.to_rgba(i) for i in d.values()],
        font_size=10,
        font_color='orange')
plt.savefig('Grafo_{0}.png'.format(main.nombre))
plt.show()
#nx.draw_kamada_kawai(G,with_labels=True,font_weight='bold',font_size=10,**options)
#plt.show()