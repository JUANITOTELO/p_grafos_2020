import networkx as nx
import os
import sys
# sys.path.insert(0, '/home/hto/Documents/vs_code/p_grafos_2020')
from networkx.drawing.nx_agraph import to_agraph 
import cell2
# define the graph as per your question
m = list(cell2.g2D[0].edges)
G=nx.MultiDiGraph(m)

# add graphviz layout options (see https://stackoverflow.com/a/39662097)
G.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
G.graph['node']={'shape':'circle'}
G.graph['graph'] = {'scale': '3'}

# adding attributes to edges in multigraphs is more complicated but see
# https://stackoverflow.com/a/26694158                    


A = to_agraph(G) 
A.node_attr["fixedsize"] = "true"
A.node_attr['style']='filled'
n = A.get_node(cell2.g[1][0])
n.attr['fillcolor']="#AAAAAA"
A.layout('dot')                                                                 
A.draw('{0}.svg'.format(cell2.g2D[1])) 
