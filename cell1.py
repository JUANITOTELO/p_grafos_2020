import igraph as ig
import netgraph, numpy, os
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import music21 as m
from os import listdir
from os.path import isfile, join
import chart_studio.plotly as py
import xlsxwriter
import pandas as pd
import plotly.graph_objs as go
from alive_progress import alive_bar
import time

def pasar_na_num(G):
    """Recibe un grafo de la libreria networkx.
       Retorna una lista con los extremos de las aristas como números."""
    Nodes = list(G.nodes)
    edges2 = list(G.edges)
    Edges = []
    for i in edges2:
        i = list(i)
        for j in range(2):
            i[j] = Nodes.index(i[j])
        i = tuple(i)
        Edges.append(i)
    return Edges

def c_2D():
    """Convierte un archivo .xml en un grafo 2 dimensional agrupando las notas y acordes pertenecientes a cada 
       compás en una lista siendo estos los vértices.
       Muestra un grafo dirigido con los vértices pintados con una escala de color que va desde los azules a 
       los rojos, siendo los azules las notas o acordes con menor grado y los rojos con mayor grado; 
       muestra también las aristas con una escala de color que va desde los blancos hasta los azules, 
       así la arista mas blanca representa el inicio de la partitura y el más azul el final.
       Retorna el grafo y el nombre del archivo"""
    aDir = os.getcwd()

    onlyfiles = [f for f in listdir('{0}/ArchiXml/'.format(aDir)) if isfile(join('{0}/ArchiXml/'.format(aDir), f))]
    for i in onlyfiles:
        print(i.replace('.xml',''))

    nombre = input("Escriba el nombre del archivo:\n")
    song = m.converter.parse('{0}/ArchiXml/{1}.xml'.format(aDir, nombre))
    print("Convirtiendo...")
    repro = input('¿Quiere reproducirlo? Si(1) No(0)')
    if(repro == 1 or repro == '1' or repro == 'si' or repro == 'Si'):
        sp = m.midi.realtime.StreamPlayer(song)
        sp.play()
    else:
        print("Ok")

    song = song.stripTies()

    # unfold repetitions
    i = 0
    for a in song:
        if a.isStream:
            e = m.repeat.Expander(a)
            s2 = e.process()
            #timing = s2.secondsMap
            #print(timing)
            song[i] = s2
        i += 1

    # todo: add note onsets


    def getMusicProperties(x):
        s = ''
        t = ''
        r = ''
        s = str(x.pitch)

        if x.tie != None:
            t = 't'
        elif(x.isRest):
            r = x.duration+'r'
        s += t+r
        s=s.replace('-','b')
        return s


    notas = []
    for a in song.recurse().notes:

        if (a.isNote):
            x = a
            s = getMusicProperties(x)
            notas.append(s)

        if (a.isChord):
            n = ''
            for x in a._notes:
                s = getMusicProperties(x)
                n += ' '+s
            notas.append(n[1:])

        if (a.isRest):
            print("hola")
            x = a
            s = getMusicProperties(x)
            notas.append(s)

    n = notas
    G = nx.DiGraph()
    for i in range(len(n)):
        if i != 0:
            G.add_edge(n[i-1], n[i])

    sn = int(input("¿Guardar grafo? No(0) Si(1)"))
    print("Listo.")

    if(sn == 1):
        pos = nx.layout.kamada_kawai_layout(G)

        d = dict(G.degree)
        low, *_, high = sorted(d.values())
        norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
        mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
        node_sizes = [v*10 for v in d.values()]
        M = G.number_of_edges()
        edge_colors = range(2, M+2)
        edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
        fig = plt.figure()
        nx.draw_networkx_nodes(
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
        nx.draw_networkx_labels(
            G,
            pos,
            font_size=10,
            font_color="white",
        )
        # set alpha value for each edge
        colorFE = []
        for i in range(M):
            edges[i].set_alpha(edge_alphas[i])
            colorFE.append(edge_alphas[i])

        # pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
        # pc.set_array(edge_colors)
        # plt.colorbar(pc)

        ax = plt.gca()
        ax.set_axis_off()
        fig.set_facecolor("#564f4f")
        fig.set_size_inches((15, 15))
        plt.savefig('{0}/GrafosImgs/Grafo_{1}.png'.format(aDir,nombre))
        print("Listo.")
        plt.show()
    
    return G, nombre

def c_3D(G, nombre):
    """Recibe un grafo en 2 dimensiones  y el nombre de la partitura y transforma el grafo 
       en uno de tres dimensiones"""
    print("Pasando grafo a formato tridimensional...")
    aDir = os.getcwd()
    d = dict(G.degree)
    
    Nodes = list(G.nodes)
    N = len(Nodes)
    Edges = pasar_na_num(G)

    Grafo = ig.Graph(Edges, directed=True)
    layt = Grafo.layout('kk', dim=3)
    Xn = [layt[k][0] for k in range(N)]  # x-coordinates of nodes
    Yn = [layt[k][1] for k in range(N)]  # y-coordinates
    Zn = [layt[k][2] for k in range(N)]  # z-coordinates
    Xe = []
    Ye = []
    Ze = []

    for e in Edges:
        Xe += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
        Ye += [layt[e[0]][1], layt[e[1]][1], None]
        Ze += [layt[e[0]][2], layt[e[1]][2], None]

    trace1 = go.Scatter3d(x=Xe,
                          y=Ye,
                          z=Ze,
                          mode='lines',
                          line=go.scatter3d.Line(
                              color="black",
                              colorscale="Blues",
                              width=3
                          ),
                          hoverinfo='none'
                          )

    trace2 = go.Scatter3d(x=Xn,
                          y=Yn,
                          z=Zn,
                          mode='markers',
                          name='notes and chords',
                          marker=dict(symbol='circle',
                                      size=6,
                                      color=list(d.values()),
                                      colorscale='Greens',
                                      line=dict(color='rgb(50,50,50)', width=0.5)
                                      ),
                          text=Nodes,
                          hoverinfo="text"
                          )

    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )

    layout = go.Layout(
        title="Grafo de la partitura {0}".format(nombre),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=1000,
        height=1000,
        showlegend=False,
        scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis),
        ),
        margin=dict(
            t=100
        ),
        hovermode='closest',
       )

    data = [trace1, trace2]
    figure = go.Figure(data=data, layout=layout)
    figure.write_html("{0}/app/templates/3D_Graph_{1}.html".format(aDir,nombre))
    print("Listo.")
    figure.show()

def c_csv(grafo1):
    """Recibe lo que retorna la función c_2D y crea un archivo csv con que contiene las columnas
       Source y Target, representando las aristas"""
    toex = pasar_na_num(grafo1[0])
    n = len(toex)
    libro = xlsxwriter.Workbook('{0}.xlsx'.format(grafo1[1]))
    hoja = libro.add_worksheet()
    row = 1
    hoja.write(0, 0, "Source")
    hoja.write(0, 1, "Target")
    print("Pasando aristas a archivo csv...")
    with alive_bar(n) as bar:
        for i in toex:
            hoja.write(row, 0, i[0]+1)
            hoja.write(row, 1, i[1]+1)
            row += 1
            time.sleep(0.02)
            bar()
    libro.close()
    read_file = pd.read_excel(r'{0}.xlsx'.format(grafo1[1]), sheet_name='Sheet1')
    read_file.to_csv (r'ArchCsv/{0}.csv'.format(grafo1[1]), index = None, header=True)
    os.system("rm {0}.xlsx".format(grafo1[1]))


#grafo1 = c_2D()
#c_csv(grafo1)
# c_3D(grafo1[0],grafo1[1])