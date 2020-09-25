import networkx as nx
import matplotlib.pyplot as plt
import main
G=nx.path_graph(main.notas)

options = {
    'node_color': 'black',
    'font_color': 'orange',
    'node_size': 260,
    'width': 1
}

print("Nodes of graph: ")
print(G.nodes())
print("Edges of graph: ")
print(G.edges())
H = nx.DiGraph(G)
nx.draw_shell(H , with_labels=True,**options)
plt.savefig("path_graph1.png")
plt.axis('off')
plt.show()