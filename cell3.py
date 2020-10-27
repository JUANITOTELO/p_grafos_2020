import networkx as nx
import os
import sys
# sys.path.insert(0, '/home/hto/Documents/vs_code/p_grafos_2020')
from networkx.drawing.nx_agraph import to_agraph
from progressbar import ProgressBar
# define the graph as per your question

class GrafoSimple:
    def crear_multigrafo(self, g, g2D):
        """Recibe como parametros una tripla de la función song_to_dict y lo que retorna la función m_graph.
           Crea un pdf del grafo."""
        
        try:
            m = list(g2D[0].edges)
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
            n = A.get_node(g[1][0])
            n.attr['fillcolor']="#32CD32"
            nf = A.get_node(g[2][-1])
            nf.attr['fillcolor']="#DC143C"


            A.layout('dot')                                                                 
            A.draw('ArchPdf/{0}.pdf'.format(g2D[1]))
        except:
            print("¡Oops!")
