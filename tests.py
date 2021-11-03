# Fonctions de test, usine à gaz et illisible mais permet de faire divers tests beaucoup plus facilement :)
from timeit import default_timer as timer
from graphes import make_graph,del_vertice,del_vertices,degrees,max_degree_vertice,edges
from approchees import algo_couplage,algo_glouton
from BB import choix_naif,branche_naif,algo_BB_naif,bornage_simple,algo_BB_bornage_simple,branche_unPeuMieux,meilleur_choix

import sys
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["figure.figsize"] = (10, 5)

def generate_instance_and_range(Nmax,nInstance,p):
    instances = {}
    pMode = "fixed"
    if isinstance(p, str):
        if p == "1/sqrt(n)":
            pMode = "1/sqrt(n)"

    nRange = np.arange(int(Nmax / 10), int(11 * Nmax / 10), int(Nmax / 10))
    for n in nRange:
        instance = []

        # Différents cas selon si on calcule p ou si il est fixé
        if pMode == "1/sqrt(n)":
            for i in range(nInstance):
                instance.append(generate_instance(n, 1 / np.sqrt(n)))
        elif pMode == "fixed":
            for i in range(nInstance):
                instance.append(generate_instance(n, float(p)))
        instances[n] = instance
    return nRange,instances

def test_func(fonction, nRange, instances, p):
    tn = []
    qn = []
    nn = []
    for n in nRange:
        instance = instances[n]
        for inst in instance:
            tnTemp=0
            if fonction not in [algo_glouton, algo_couplage]:
                start = timer()
                C, qnRes, nnRes = fonction(inst)
                end = timer()
                tnTemp += end - start

            else:
                start = timer()
                C, qnRes = fonction(inst)
                end = timer()
                nnRes = 0
                tnTemp += end - start
                
        tn.append(tnTemp / len(instance))
        qn.append(qnRes)
        nn.append(nnRes)

    return nRange, tn, qn, nn


def test_funcs(fonctions, Nmax, nInstance, p):
    resTestFunctions = []
    nRange,instances = generate_instance_and_range(Nmax,nInstance,p)
    for f in fonctions:
        resTestf = test_func(f, nRange, instances, p)
        resTestFunctions.append(resTestf)
    return resTestFunctions


def trace_time2(functions, resTestFunctions, p,echelle="linear"):
    for i in range(len(functions)):
        plt.plot(
            resTestFunctions[i][0], resTestFunctions[i][1], label=functions[i].__name__
        )
        plt.yscale(echelle)

    if not isinstance(p, str):
        ptitle = str(p)
    else:
        ptitle = p

    plt.title(
        "Temps d'exé. en sec en fonc. du nombre de sommets n avec une proba. de présence d'arêtes p="
        + ptitle
    )
    plt.xlabel("Nombre de sommets")
    plt.ylabel("Temps moyen d'exécution (s)")
    plt.legend(loc="upper left")
    plt.show()


def trace_quality(functions, resTestFunctions, p):
    for i in range(len(functions)):
        plt.plot(
            resTestFunctions[i][0], resTestFunctions[i][2], label=functions[i].__name__
        )

    if not isinstance(p, str):
        ptitle = str(p)
    else:
        ptitle = p

    plt.title(
        "Taille de la couverture retournée en fonc. du nombre de sommets n avec une proba. de présence d'arêtes p="
        + ptitle
    )
    plt.xlabel("Nombre de sommets")
    plt.ylabel("Taille de la couverture")
    plt.legend(loc="upper left")
    plt.show()


def trace_nNode(functions, resTestFunctions, p):
    atLeastOne = False
    for i in range(len(functions)):
        if sum(resTestFunctions[i][3]) > 0:
            atLeastOne = True
            plt.plot(
                resTestFunctions[i][0],
                resTestFunctions[i][3],
                label=functions[i].__name__,
            )
            plt.yscale("log")

    if atLeastOne:
        if not isinstance(p, str):
            ptitle = str(p)
        else:
            ptitle = p

        plt.title(
            "Nombre de noeuds générés en fonc. du nombre de sommets n avec une proba. de présence d'arêtes p="
            + ptitle
        )
        plt.xlabel("Nombre de sommets")
        plt.ylabel("Nombre de noeuds générés")
        plt.legend(loc="upper left")
        plt.show()


def procedure_tests(nMax, nG, functions):

    resTestp = []
    for p in [0.5, 0.8]:
        resTestFunctions = test_funcs(functions, nMax, nG, p)
        resTestp.append([functions, resTestFunctions, p])
    resTestFunctions = test_funcs(functions, nMax, nG, "1/sqrt(n)")
    resTestp.append([functions, resTestFunctions, "1/sqrt(n)"])

    for resTestpIns in resTestp:
        trace_time2(resTestpIns[0], resTestpIns[1], resTestpIns[2])
    for resTestpIns in resTestp:
        trace_quality(resTestpIns[0], resTestpIns[1], resTestpIns[2])
    for resTestpIns in resTestp:
        trace_nNode(resTestpIns[0], resTestpIns[1], resTestpIns[2])

def procedure_testsSPEED(nMax, nG, functions):

    resTestp = []
    for p in [0.5]:
        resTestFunctions = test_funcs(functions, nMax, nG, p)
        resTestp.append([functions, resTestFunctions, p])
    resTestFunctions = test_funcs(functions, nMax, nG, "1/sqrt(n)")
    resTestp.append([functions, resTestFunctions, "1/sqrt(n)"])

    for resTestpIns in resTestp:
        trace_time2(resTestpIns[0], resTestpIns[1], resTestpIns[2],"log")


# Wrappers
def Algo_BB_naif(G):
    return algo_BB_naif(G, choix_naif, branche_naif)


def Algo_BB_bornage_simple(G):
    return algo_BB_bornage_simple(G, choix_naif, branche_naif, bornage_simple)


def Algo_BB_bornage_simple_meilleure_branche(G):
    return algo_BB_bornage_simple(G, choix_naif, branche_unPeuMieux, bornage_simple)


def Algo_BB_bornage_simple_meilleurs_choixEtBranche(G):
    return algo_BB_bornage_simple(G, meilleur_choix, branche_unPeuMieux, bornage_simple)



functions = [algo_glouton, algo_couplage]
procedure_tests(350, 20, functions)
functions = [algo_glouton, algo_couplage,Algo_BB_bornage_simple_meilleurs_choixEtBranche]
procedure_tests(100,20,functions)

functions = [Algo_BB_naif]
procedure_tests(20,20,functions)
functions = [Algo_BB_naif, Algo_BB_bornage_simple]
procedure_tests(20,20,functions)

functions = [Algo_BB_bornage_simple, Algo_BB_bornage_simple_meilleure_branche]
procedure_tests(20,20,functions)
functions = [Algo_BB_bornage_simple_meilleure_branche]
procedure_tests(80,20,functions)
functions = [
    Algo_BB_bornage_simple_meilleure_branche,
    Algo_BB_bornage_simple_meilleurs_choixEtBranche,
]
procedure_tests(80,20,functions)
functions = [Algo_BB_bornage_simple_meilleurs_choixEtBranche]
procedure_tests(100,20,functions)


functions = [
    algo_glouton,
    algo_couplage,
    Algo_BB_naif,
    Algo_BB_bornage_simple,
    Algo_BB_bornage_simple_meilleure_branche,
    Algo_BB_bornage_simple_meilleurs_choixEtBranche,
]

procedure_testsSPEED(100, 1, functions)
