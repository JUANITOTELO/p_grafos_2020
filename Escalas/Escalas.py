import networkx as nx
import netgraph
import math
import matplotlib.colors as mc
import matplotlib.pyplot as plt
import numpy as np
import music21 as m
import os

def getMusicProperties(x):
    """ Recibe ya sea una nota o un acorde y lo convierte en una cadena te texto."""
    s = ''
    t=''
    r=''
    s = str(x.pitch)
    if x.tie != None:
        t = 't'
    elif(x.isRest):
        r = x.duration+'r'
    s += t+r
    return s

def crear_escala(mM,nota):
    """ Recibe si la escala es mayor o menor y desde que nota empezar a crear la escala.
        Guarda las escalas en forma de grafo en un png."""
    aDir=os.getcwd()
    song = m.converter.parse('{0}/ArchiXml/{1}.xml'.format(aDir,"Escala Cromática"))
    #sp = m.midi.realtime.StreamPlayer(song)
    #sp.play()
    # process the ties
    song = song.stripTies()

    # unfold repetitions
    i = 0
    for a in song:
        if a.isStream:
            e = m.repeat.Expander(a)
            s2 = e.process()
            # timing = s2.secondsMap
            song[i] = s2
        i += 1

    # todo: add note onsets

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
            x = a
            s = getMusicProperties(x)
            notas.append(s)

    n = notas[0:12]
    nombre = n[nota]
    n = n[nota::]+n[0:nota]
    if mM == "m":
        nums = [n[1],n[4],n[6],n[9],n[11]]
        for i in nums:
            n.remove(i)
    elif mM == "M":
        nums = [n[1],n[3],n[6],n[8],n[10]]
        for i in nums:
            n.remove(i)

    n = n[::-1]
    G = nx.DiGraph()
    for i in range(len(n)):
        n[i-1] = n[i-1].replace('4', '')
        n[i] = n[i].replace('4', '')
        # if i != 0:
        G.add_edge(n[i-1], n[i])
    pos = nx.layout.shell_layout(G, rotate= np.pi/2)
    nodesColors = []
    for i in G.nodes:
        if("#" in i):
            nodesColors.append("#000000")
        else:
            nodesColors.append("#fffce2")
    
    inter = []
    if mM == "m":
        inter = ["1","1","1/2","1","1","1/2","1"]
    elif mM == "M":
        inter = ["1/2","1","1","1","1/2","1","1"]
    else:
        for i in range(len(list(G.edges))):
            inter.append("1/2")
    inter = dict(zip(G.edges,inter))
    fig = plt.figure()
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=900,
        node_color=nodesColors
    )
    nx.draw_networkx_edges(
        G,
        pos,
        node_size=900,
        arrowstyle="<-",
        arrowsize=10,
        width=4,
        connectionstyle="arc3,rad=0.2",
        
    )
    
    nx.draw_networkx_edge_labels(G,pos,edge_labels=inter,rotate=False)
    
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=18,
        font_weight="bold",
        font_color="#059eb0",
    )


    ax = plt.gca()
    ax.set_axis_off()
    fig.set_size_inches((10, 10))
    fig.set_facecolor("#4f4f4f00")
    if mM == "m":
        plt.savefig('Escalas/EscalasMenores/Escala_menor_natural_de_{0}.pdf'.format(nombre.replace('4', '')))
        plt.close(fig=fig)
        plt.clf()
    elif mM == "M":
        plt.savefig('Escalas/EscalasMayores/Escala_Mayor_de_{0}.pdf'.format(nombre.replace('4', '')))
        plt.close(fig=fig)
        plt.clf()
    else:
        plt.savefig('Escalas/Escala_cromática_desde_{0}.pdf'.format(nombre.replace('4', '')))
        plt.close(fig=fig)
        plt.clf()
    # plt.show()
