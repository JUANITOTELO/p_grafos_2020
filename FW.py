import cell1, cell2, cell3
import networkx as nx
import os
import matplotlib.pyplot as plt
import matplotlib as mpl

def print_solution(distance,s):
    """ Recibe una matriz distance y el tamaño de esta.
        Imprime la matriz de en consola."""
    for i in range(s):
        for j in range(s):
            if(distance[i][j] == 9999999):
                print("INF", end=" ")
            else:
                print(distance[i][j], end="  ")
        print(" ")

def centro_FW(G,nombre):
    """Recibe un grafo de la librería networkx y el nombre del grafo.
       Muestra el centro en un png."""
    A = nx.to_numpy_array(G)
    s = len(A)
    #Elimino los ciclos del grafo y asigno infinitos
    for i in range(s):
        A[i][i] = 0
        for j in range(s):
            if A[i][j] == 0 and i != j:
                A[i][j] = 9999999
    distance = list(map(lambda i: list(map(lambda j: j, i)), A))

    # Adding vertices individually
    for k in range(s):
        for i in range(s):
            for j in range(s):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
    Nodes = list(G.nodes)
    Edges = []
    excentricidades = []
    c = 0
    f = 0
    for i in distance:
        n = 0
        for j in i:
            if j > n and j != 9999999.0:
                n = j
            c += 1
        if n != 0:
            excentricidades.append(n)
        c = 0
        f += 1
    

    c = 0
    f = 0
    rad = min(excentricidades)
    for i in distance:
        n = 0
        nf = ""
        nc = ""
        for j in i:
            if j > n and j != 9999999.0:
                n = j
                nf = Nodes[f]
                nc = Nodes[c]
            c += 1
        if n == rad:
            Edges.append((nf,nc))
        c = 0
        f += 1

    aDir = os.getcwd()
    cen = nx.DiGraph()
    cen.add_edges_from(Edges)
    pos = nx.layout.kamada_kawai_layout(cen)
    sf = 7
    sn = 25
    d = dict(cen.degree)
    low, *_, high = sorted(d.values())
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.winter)
    node_sizes = [v*sn for v in d.values()]
    M = cen.number_of_edges()
    edge_colors = range(2, M+2)
    edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
    fig = plt.figure()
    nx.draw_networkx_nodes(
        cen,
        pos,
        node_size=node_sizes,
        node_color=[mapper.to_rgba(i) for i in d.values()]
    )
    edgesC = nx.draw_networkx_edges(
        cen,
        pos,
        node_size=node_sizes,
        arrowstyle="wedge",
        arrowsize=10,
        edge_color=edge_colors,
        edge_cmap=plt.cm.Blues,
        #connectionstyle="arc3,rad=0.1",
        width=2,
    )

    nx.draw_networkx_labels(
        cen,
        pos,
        font_size=sf,
        font_weight="bold",
        font_color="#0f1010",
    )
    # set alpha value for each edge
    # colorFE = []
    for i in range(M):
        edgesC[i].set_alpha(edge_alphas[i])
        # colorFE.append(edge_alphas[i])

    # pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
    # pc.set_array(edge_colors)
    # plt.colorbar(pc)

    ax = plt.gca()
    ax.set_axis_off()
    fig.set_facecolor("#f1f6f400")
    # #564f4f
    fig.set_size_inches((7, 7))
    plt.savefig('{0}/ArchPdf/centro_de_{1}.pdf'.format(aDir, nombre))
    plt.show()
    plt.clf()

    # cell3.GrafoSimple().crear_multigrafo((cen, "Centro-de-{0}".format(nombre)))