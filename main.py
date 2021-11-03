from graphes import make_graph,del_vertice,del_vertices,degrees,max_degree_vertice,edges
from approchees import algo_couplage,algo_glouton
from BB import choix_naif,branche_naif,algo_BB_naif,bornage_simple,algo_BB_bornage_simple,branche_unPeuMieux,meilleur_choix

import sys
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

# Tests sur instances simples pour être sûr d'avoir les bons résultats (ces instances sont illustrées dans le rapport)

if len(sys.argv)==2:
    nomFichier = sys.argv[1]
    test = make_graph(nomFichier)
    print("Graphe lu")
    print(test)
    print()
    print("Algo_couplage")
    print(algo_couplage(test))
    print("Algo_glouton")
    print(algo_glouton(test))
    print("Algo_BB_naif")
    print(algo_BB_naif(test, choix_naif, branche_naif))
    print("Algo_BB_bornage_simple")
    print(algo_BB_bornage_simple(test, choix_naif, branche_naif, bornage_simple))
    print("Algo_BB_bornage_simple et meilleur branchement")
    print(algo_BB_bornage_simple(test, choix_naif, branche_unPeuMieux, bornage_simple))
    print("Algo_BB_bornage_simple, meilleur choix et meilleur branchement")
    print(
        algo_BB_bornage_simple(test, meilleur_choix, branche_unPeuMieux, bornage_simple)
    )
    print("Fin test")
else:
    print("En l'absence d'argument satisfaisant, je fais tourner les exemples de bases...")
    print()
    sleep(3)
    test1 = make_graph("exempleinstance.txt")
    print("Graphe 1 : " + str(test1))
    test2 = make_graph("exempleinstance2.txt")
    print("Graphe 2 : " + str(test2))
    test3 = make_graph("exempleinstance3.txt")
    print("Graphe 3 : " + str(test3))
    test4 = make_graph("exempleinstance4.txt")
    print("Graphe 4 : " + str(test4))
    print()
    print()
    print("Début des tests")
    for test in [test1, test2, test3,test4]:
        print("Algo_couplage")
        print(algo_couplage(test))
        print("Algo_glouton")
        print(algo_glouton(test))
        print("Algo_BB_naif")
        print(algo_BB_naif(test, choix_naif, branche_naif))
        print("Algo_BB_bornage_simple")
        print(algo_BB_bornage_simple(test, choix_naif, branche_naif, bornage_simple))
        print("Algo_BB_bornage_simple et meilleur branchement")
        print(algo_BB_bornage_simple(test, choix_naif, branche_unPeuMieux, bornage_simple))
        print("Algo_BB_bornage_simple, meilleur choix et meilleur branchement")
        print(
            algo_BB_bornage_simple(test, meilleur_choix, branche_unPeuMieux, bornage_simple)
        )
        print("Fin test")
        print()
