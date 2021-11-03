from graphes import make_graph,del_vertice,del_vertices,degrees,max_degree_vertice,edges
from approchees import algo_couplage,algo_glouton

import matplotlib.pyplot as plt
import numpy as np

#=======================================Algorithme naif========================================


# Retourne la première arête non couverte qu'il trouve, renvoie None si toutes sont couvertes.
# Ne fait pas grand chose ici, mais sera utile par la suite pour ne pas ré-écrire tout le B&B
def choix_naif(G, C):
    pickedVertexU = next((s for s in G if (s not in C) and G[s]), None)
    if pickedVertexU == None:
        return None
    else:
        pickedVertexV = next((t for t in G[pickedVertexU] if t not in C))
        return (pickedVertexU, pickedVertexV)


# Branchement à gauche ou à droite, selon le paramètre side = "l" ou "r"
# Ce branchement est naïf, et il branche juste (u,v) en mettant u à gauche et v à droite
def branche_naif(currentGraph, pickedEdge, bestScore, bestC, side):
    if side == "r":
        pickedIndice = 1
    else:  # side == 'l'
        pickedIndice = 0

    score = currentGraph[0] + 1
    computedC = currentGraph[1] + [pickedEdge[pickedIndice]]
    remaining = del_vertice(currentGraph[2], pickedEdge[pickedIndice])

    return (score, computedC, remaining)


# Algorithme de branch and bound sans bornes tel que décrit dans le sujet partie 4.1
# Voir rapport pour justification de l'implémentation itérative
def algo_BB_naif(G, func_choix, func_branch):
    # Init
    G = {i:j for i,j in G.items() if j != []} #On peut supprimer les sommets isolés : Ils ne seront de toute façon pas dans la couverture !
    bestScore = np.inf
    bestC = list(G.keys())
    stack = [(0, [], G)]  # Score, solution construite, graphe restant
    nNodes = 1
    while stack:
        currentGraph = stack.pop()
        pickedEdge = func_choix(currentGraph[2], currentGraph[1])
        if pickedEdge == None:  # On a atteint une feuille
            continue

        # Branchement
        nNodes += 2
        rBranch = func_branch(currentGraph, pickedEdge, bestScore, bestC, "r")
        lBranch = func_branch(currentGraph, pickedEdge, bestScore, bestC, "l")
        for branch in [
            rBranch,
            lBranch,
        ]:  # L'ordre importe peu pour le moment, mais importera par la suite !
            if not branch[2]:  # dict vide
                if branch[0] < bestScore:  # meilleur score
                    bestC = branch[1]
                    bestScore = branch[0]
            else:
                stack.append(branch)

    return bestC, bestScore, nNodes
    
#=======================================Algorithme avec bornes========================================

# Implémentation des bornes tel que décrites dans le sujet 4.2
# Il manque b2, voir rapport
def bornage_simple(G, score):
    n = len(G)
    m = sum(len(v) for v in G.values()) / 2
    b1 = np.ceil(m / max(degrees(G)[0]))
    if (2 * n - 1) ** 2 - 8 * m < 0:  # Négatif sur les petits graphes
        b3 = 0
    else:
        b3 = (2 * n - 1 - np.sqrt((2 * n - 1) ** 2 - 8 * m)) / 2
    minScore = max(b1, b3)
    couplage, maxScore = algo_couplage(G)
    return (
        maxScore + score,
        minScore + score,
        couplage,
    )  # maxScore et scoreCouplage = même chose, donc pas la peine de retourner le score du couplage


# Cette fois on utilise les bornes calculés en chaque noeud tel que décrit dans bornage_simple, et on élague si besoin est
def algo_BB_bornage_simple(G, func_choix, func_branch, func_borne):
    #Init
    G = {i:j for i,j in G.items() if j != []} #On peut supprimer les sommets isolés : Ils ne seront de toute façon pas dans la couverture !
    bestC, bestScore = algo_couplage(G)
    stack = [(0, [], G)]
    nNodes = 1
    while stack:
        currentGraph = stack.pop()
        pickedEdge = func_choix(currentGraph[2], currentGraph[1])
        if pickedEdge == None:  # On a atteint une feuille
            continue

        # Branchement
        nNodes += 2
        rBranch = func_branch(currentGraph, pickedEdge, bestScore, bestC, "r")
        lBranch = func_branch(currentGraph, pickedEdge, bestScore, bestC, "l")

        for branch in [rBranch, lBranch]:
            if not branch[2]:  # dict vide
                if branch[0] < bestScore:  # meilleur score
                    bestC = branch[1]
                    bestScore = branch[0]
            else:
                maxScoreBranch, minScoreBranch, couplage = bornage_simple(
                    branch[2], branch[0]
                )
                if (minScoreBranch == maxScoreBranch) or (minScoreBranch > bestScore):
                    # On élague, on prend potentiellement le couplage comme solution si c'est le mimnimum possible
                    if maxScoreBranch < bestScore:
                        bestC = couplage
                        bestScore = maxScoreBranch
                else:  # On peut encore tenter de faire mieux, on continue d'explorer
                    stack.append(branch)

    return bestC, bestScore, nNodes

#=======================================Amélioration du branchement========================================

def branche_unPeuMieux(currentGraph, pickedEdge, bestScore, bestC, side):
    if side == "r":
        # On prend tous les voisins de u
        neighbours = currentGraph[2][pickedEdge[0]]
        score = currentGraph[0] + len(neighbours)
        computedC = currentGraph[1] + neighbours
        remaining = del_vertices(currentGraph[2], neighbours)
    else:  # side == 'l'
        # On prend seulement u
        score = currentGraph[0] + 1
        computedC = currentGraph[1] + [pickedEdge[0]]
        remaining = del_vertice(currentGraph[2], pickedEdge[0])

    return (score, computedC, remaining)
    
#=======================================Amélioration du choix de sommets qui font les noeuds========================================

# On ne prend plus u à gauche et v à droite pour (u,v), mais on prend le degré maximum à gauche et le minimum à droite

# C'est ici que l'ordre de traitement des branches dans algo_BB est important. En faisant ce choix de branchement,
# on retrouvera beaucoup plus souvent la solution optimale dans la branche de droite que dans celle de gauche.
# Il faut donc s'occuper de la branche de droite avant celle de gauche !
def meilleur_choix(G, C):
    pickedVertexU = max_degree_vertice(G)
    if pickedVertexU == None:
        return None
    else:
        pickedVertexV = next((t for t in G[pickedVertexU] if t not in C))
        return (pickedVertexU, pickedVertexV)
