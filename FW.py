import cell1, cell2, cell3
import networkx as nx
import matplotlib.pyplot as plt

def print_solution(distance,s):
    for i in range(s):
        for j in range(s):
            if(distance[i][j] == 9999999):
                print("INF", end=" ")
            else:
                print(distance[i][j], end="  ")
        print(" ")

def centro_FW(G,nombre):
    """Recibe un grafo de la libreria networkx.
       Muestra el centro.
       Retorna en una lista las aristas que generan el centro del grafo."""
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
    # print_solution(distance,s)
    Nodes = list(G.nodes)
    Edges = []
    c = 0
    f = 0
    for i in distance:
        for j in i:
            if j == 1:
                Edges.append((Nodes[f],Nodes[c]))
            c += 1
        c = 0
        f += 1
    cen = nx.DiGraph()
    cen.add_edges_from(Edges)
    cell3.GrafoSimple().crear_multigrafo((cen, "Centro-de-{0}".format(nombre)))
