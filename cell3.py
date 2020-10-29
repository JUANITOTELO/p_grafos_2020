import networkx as nx
import os
import sys
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph


class GrafoSimple:
    def crear_multigrafo(self, g2D):
        """Recibe como parametros una tripla de la función song_to_dict y lo que retorna la función m_graph.
           Crea un pdf del grafo."""
        
        try:
            m = list(g2D[0].edges)
            n = list(g2D[0].nodes)
            G=nx.MultiDiGraph(m)

            G.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
            G.graph['node']={'shape':'circle'}
            G.graph['graph'] = {'scale': '3'}

            A = to_agraph(G) 
            A.node_attr["fixedsize"] = "true"
            A.node_attr['style']='filled'
            ni = A.get_node(n[0])
            ni.attr['fillcolor']="#32CD32"
            nf = A.get_node(n[-1])
            nf.attr['fillcolor']="#DC143C"


            A.layout('dot')                                                       
            A.draw('ArchPdf/{0}.pdf'.format(g2D[1]))
        except:
            print("¡Oops!")
