import cell1
import igraph as ig
import music21 as m
import networkx as nx
from os import listdir
import matplotlib as mpl
import netgraph
import numpy
from progressbar import progressbar
from alive_progress import alive_bar
import time
import os
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from os.path import isfile, join
import chart_studio.plotly as py
import matplotlib.animation as animation


def song_to_dict():
    """Convierte la partitura en un diccionario que incluye los instrumentos numerados del 0 hasta el total de
       instrumentos-1, compaces, notas y acordes de todo el documento,
       retornando una tripla con el diccionario, una lista con todas las notas y otra con los acordes y por último el nombre"""
    aDir = os.getcwd()
    archivos = listdir('{0}/ArchiXml/'.format(aDir))
    onlyfiles = []
    for f in progressbar(archivos):
        if isfile(join('{0}/ArchiXml/'.format(aDir), f)):
            onlyfiles.append(f)
        time.sleep(0.02)
    # Imprimir archivos disponibles
    for i in onlyfiles:
        print(i.replace('.xml', ''))
        

    nombre = input("Escriba el nombre del archivo:\n")
    song = m.converter.parse('{0}/ArchiXml/{1}.xml'.format(aDir, nombre))
    print("Separando archivo por partes...")
    
    partes = []
    compaces = []
    notas = []
    acordes = []
    # print(partes["piano"])
    # print(partes["piano"]["compas 1"])
    # print(partes["piano"]["compas 1"]["notas"])
    # print(partes["piano"]["compas 1"]["notas"][0])
    # print(partes["piano"]["compas 1"]["acordes"])
    # print(partes["piano"]["compas 1"]["acordes"][0])
    for i in song.parts:
        
        parte = ""
        if i.partName == None:
            parte = "piano"
        else:
            parte = str(i.partName)
        partes.append(parte)
        #print(parte)
        temCompaces = []
        for j in progressbar(i.recurse().getElementsByClass('Measure')):
            numer = int(j.number)
            compa = "M{0}".format(numer)
            temNotas = []
            temAcordes = []
            for k in j.recurse().getElementsByClass('Note'):
                temNotas.append(str(k.nameWithOctave.replace("-", "b")))
            for k in j.recurse().getElementsByClass('Chord'):
                n = ''
                for l in k.notes:
                    n += ' '+l.nameWithOctave.replace("-", "b")
                temAcordes.append(n[1:])
            if(temNotas != [] or temAcordes != []):
                temCompaces.append(
                    {compa: {"notas": temNotas, "acordes": temAcordes}})
            notas += temNotas
            acordes += temAcordes
            time.sleep(0.02)
        compaces.append(temCompaces)

    c = 1
    print("Agrupando los compaces...")
    Compaces = []
    for i in progressbar(compaces):
        if i != []:
            xx = i[0]
            for f in range(len(i)-1):
                yy = i[f+1]
                xx.update(yy)
            Compaces.append(xx)
        time.sleep(0.02)

    cancion = {}
    o = len(Compaces)
    for i in progressbar(range(o-1)):
        partes[i] = (c-1)
        partes[i+1] = c
        c += 1
        time.sleep(0.02)

    for i in progressbar(range(o)):
        cancion.update({partes[i]: Compaces[i]})
        time.sleep(0.02)
#     print("Compaces, notas y acordes de {0}:\n{1}".format(nombre,cancion))
#     print("Notas de {0}:\n{1}".format(nombre,notas))
#     print("Acordes de {0}:\n{1}".format(nombre,acordes))
    print("Listo.")
    return cancion, notas, acordes, nombre


def m_graph(n, nombre):
    """Recibe una lista con los vertices del grafo y el nombre del archivo, lo convierte en un grafo 2 dimensional.
       Retorna el grafo y el nombre del archivo."""
    video = int(input("¿paso a paso? si(1) no(0)\n Si selecciona si(1) se requiere de bastante memoria RAM.\n"))
    print("Convirtiendo grafo a formato 2-dimensional...")
    aDir = os.getcwd()
    G = nx.DiGraph()
    if(video == 1):
        for i in range(len(n)):
            if i != 0:
                G.add_edge(n[i-1], n[i])

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
                    # G,
                    # pos,
                    # node_size=node_sizes,
                    # arrowstyle="wedge",
                    # arrowsize=10,
                    # edge_color=edge_colors,
                    # edge_cmap=plt.cm.Blues,
                    # width=2,
                    G,
                    pos,
                    node_size=node_sizes,
                    arrowstyle="wedge",
                    arrowsize=10,
                    edge_color=edge_colors,
                    edge_cmap=plt.cm.Blues,
                    #connectionstyle="arc3,rad=0.2",
                    width=3,
                )
                nx.draw_networkx_labels(
                    G,
                    pos,
                    font_size=12,
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
                fig.set_size_inches((10, 10))
                plt.savefig(
                    '{0}/prVideo/Grafo_{1}_{2}.png'.format(aDir, nombre, i))
                print("Listo.")
                plt.clf()
                plt.close("all")
    else:
        with alive_bar(len(n),spinner = 'notes2') as bar:
            for i in range(len(n)):
                if i != 0:
                    G.add_edge(n[i-1], n[i])
                time.sleep(0.002)
                bar()
        
        pos = nx.layout.kamada_kawai_layout(G)
        sf = 7
        sn = 10
        tn = len(n)
        if(tn <= 40):
            sf = 15
            sn = 100
        d = dict(G.degree)
        try:
            low, *_, high = sorted(d.values())
            norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
            mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)

            node_sizes = [v*sn for v in d.values()]
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
                #connectionstyle="arc3,rad=0.1",
                width=2,
            )
        
            nx.draw_networkx_labels(
                G,
                pos,
                font_size=sf,
                font_color="white",
            )
            # set alpha value for each edge
            # colorFE = []
            for i in range(M):
                edges[i].set_alpha(edge_alphas[i])
                # colorFE.append(edge_alphas[i])

            # pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
            # pc.set_array(edge_colors)
            # plt.colorbar(pc)

            ax = plt.gca()
            ax.set_axis_off()
            fig.set_facecolor("#564f4f")
            fig.set_size_inches((10, 10))
            plt.savefig('{0}/GrafosImgs/grafo_{1}.png'.format(aDir, nombre))
            print("Listo.")
            #plt.show()
            plt.clf()
            plt.close("all")
        except:
            print("Hubo un error.")

    return G, nombre


#g = song_to_dict()

#n0 = []
#for i in range(len(g[0][0])):
#    if ('M{0}'.format(i+1) in g[0][0]):
#        n0 += g[0][0]['M{0}'.format(i+1)]['notas']
    
#print(n0)
#g2D = m_graph(n0, g[3])
#cell1.c_3D(g2D[0],g2D[1])
