import matplotlib.pyplot as plt
import numpy as np


# Fonction de lecture
def make_graph(nomFichier):
    filein = open(nomFichier, "r")
    lines = filein.readlines()
    graph = {}
    mode = ""
    nedge = 0
    for line in lines:
        if line == "Nombre de sommets\n":
            mode = "nVert"
            continue
        elif line == "Sommets\n":
            mode = "vert"
            continue
        elif line == "Nombre d aretes\n":
            mode = "nEdge"
            continue
        elif line == "Aretes\n":
            mode = "edge"
            continue
        else:
            if mode == "vert":
                graph[line.split()[0]] = []
            elif mode == "nVert":
            	#print(graph)
            	continue
            elif mode == "edge":
                s = line.split()[0]
                t = line.split()[1]
                graph[s].append(t)
                graph[t].append(s)

    filein.close()
    return graph

# Si on a python 3.10, on peut utiliser la toute nouvelle syntaxe match-case. Mais comme cette version est récente, je ne l'utilise pas par sécurité.
# Je laisse ici quelques lignes, à titre d'exemple, qui remplaceraient les if elif de make_graph()

"""
match line:
        case 'Sommets':
            mode = 'som'
            continue
        case 'Aretes' :
            mode = 'are'
            continue
        case _ :
            match mode:
                case :
                ...
                        
"""

# Enlève le sommet v du graphe G (Et renvoie le résultat dans un nouveau graphe)
def del_vertice(G, v):

    Gfiltered = G.copy()
    if v in Gfiltered:
        removed = Gfiltered.pop(v)
        for vertice in removed:
            Gfiltered[vertice] = list(filter(v.__ne__, Gfiltered[vertice]))
            if not Gfiltered[vertice]:
                    Gfiltered.pop(vertice)
    return Gfiltered

# Enlève les sommets de V du graphe G (Et renvoie le résultat dans un nouveau graphe)
def del_vertices(G, V):
    Gfiltered = G.copy()
    for v in V:
        if v in Gfiltered:
            removed = Gfiltered.pop(v)
            for vertice in removed:
                Gfiltered[vertice] = list(filter(v.__ne__, Gfiltered[vertice]))
                if not Gfiltered[vertice]:
                    Gfiltered.pop(vertice)
    return Gfiltered

from collections import defaultdict

# Retourne les degrés des sommets de G, sous forme de list puis sous forme de dict
# Premier retour pour respecter la consigne, deuxième retour plus pratique pour la suite selon moi, utilise defaultdict pour une petite conversion
def degrees(G):
    degrees = []
    degrees2 = defaultdict(list)
    for vertice in G:
        degrees.append(len(G[vertice]))
        degrees2[len(G[vertice])].append(vertice)
    return degrees, dict(degrees2)


# Retourne le sommet ayant le plus haut degré dans G
def max_degree_vertice(G):
    if not G:
        return None
    else:
        dictDegrees = degrees(G)[1]
        return dictDegrees[max(dictDegrees.keys())][0]

# Fonction auxiliaire qui permet un meilleur accès si on veut itérer par aretes et non pas par sommets, comme dans les deux algos suivants.
# Pas besoin de déduire le temps d'exécution car il est plus petit que l'écart type du temps d'exécution des algos qui utilisent cette fonction
def edges(G):
    res = []
    for s in G:
        for t in G[s]:
            res.append((s, t))
    return res
