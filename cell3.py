import networkx as nx
import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
from networkx.drawing.nx_agraph import to_agraph


class GrafoSimple:
    def crear_multigrafo(self, g2D):
        """ Recibe como parametros una tripla de la función song_to_dict y lo que retorna la función m_graph.
            Crea un pdf del grafo."""
    
        aDir = os.getcwd()
        G = g2D[0]
        nombre = g2D[1]
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        sn = 10
        d = dict(G.degree)
        low, *_, high = sorted(d.values())
        norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
        mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.winter)

        node_sizes = [v*sn for v in d.values()]
        M = G.number_of_edges()
        edge_colors = range(2, M+2)
        fig = plt.figure()
        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=node_sizes,
            node_color=[mapper.to_rgba(i) for i in d.values()]
        )
        nx.draw_networkx_edges(
            G,
            pos,
            node_size=node_sizes,
            arrowstyle="wedge",
            arrowsize=10,
            edge_color=edge_colors,
            edge_cmap=plt.cm.Blues,
            connectionstyle="arc3,rad=0.1",
            width=2,
        )
    
        nx.draw_networkx_labels(
            G,
            pos,
            font_size=7,
            font_color="white",
        )
        # set alpha value for each edge
        # colorFE = []
        # for i in range(M):
        #     edges[i].set_alpha(edge_alphas[i])
        #     # colorFE.append(edge_alphas[i])

        # pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
        # pc.set_array(edge_colors)
        # plt.colorbar(pc)

        ax = plt.gca()
        ax.set_axis_off()
        fig.set_facecolor("#00225800")
        # #564f4f
        fig.set_size_inches((10, 10))
        pd = int(input("¿Guardar? si(1) no(0)\n"))
        if pd == 1:
            opt = int(input("(1)pdf\n(2)png\n(3)svg\n"))
            if opt == 1:
                plt.savefig('{0}/ArchPdf/grafo_{1}.pdf'.format(aDir, nombre))
                plt.show()
                
            elif opt == 2:
                plt.savefig('{0}/GrafosImgs/grafo_{1}.png'.format(aDir, nombre))
                plt.show()
                
            elif opt == 3:
                plt.savefig('{0}/ArchSvg/grafo_{1}.svg'.format(aDir, nombre))
                plt.show()
        plt.clf()
        print("Listo.") 


