from graphes import make_graph,del_vertice,del_vertices,degrees,max_degree_vertice,edges

import matplotlib.pyplot as plt
import numpy as np

def algo_couplage(G):
    C = []
    edgs = edges(G)
    for (s, t) in edgs:
        if s not in C and t not in C:
            C.extend([s, t])
    return C, len(C)
    
def algo_glouton(G):
    C = []
    edgs = edges(G)
    dictDegrees = degrees(G)[1]
    while edgs:
        # Trouve le max
        maxDegree = max(list(dictDegrees.keys()))
        maxVert = dictDegrees[maxDegree].pop(0)
        # MAJ du dictionnaire
        if not dictDegrees[maxDegree]:
            dictDegrees.pop(maxDegree)

        # On ajoute le sommet et on trie pour garder les arêtes non-couvertes
        C.append(maxVert)
        edgs[:] = [edge for edge in edgs if maxVert not in edge]
    return C, len(C)
