import networkx as nx
import netgraph
import matplotlib.pyplot as plt
import numpy
import main
options = {
    'node_color': 'black',
    'font_color': 'orange',
    'node_size': 800,
    'width': 1.5
}
n = main.notas
G = nx.Graph()
for i in range(len(n)):
    n[i-1]=n[i-1].replace('4','')
    n[i]=n[i].replace('4','')
    if i != 0:
        G.add_edge(n[i-1],n[i])
print(n)
nx.draw_kamada_kawai(G,with_labels=True,font_weight='bold',font_size=10,**options)
plt.savefig('Grafo_{0}.png'.format(main.nombre))
plt.show()
