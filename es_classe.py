"""
Dato un grafo $G = (V, E)$, con capacita' su gli archi pari ad $h_{ij}$ per ogni arco $(i, j) in E$,
domanda (positiva o negativa) pari a $b_i$ per ogni nodo $i in V$, e costo unitario del flusso $c_{ij}$ per ogni arco $(i, j) in E$ il problema
del flusso a costo minimo consiste nel trovare un flusso che rispetti tutte le domande a costo minimo.

Cominciamo con il generare in modo casuale un grafo $G$ (per facilitare la riproduzione dei risultati e'
consigliabile fissare il seed del generatore di numeri casuali utilizzati, ad esempio usando np.random.seed) con almeno 150 nodi.

Generiamo inoltre le capacita' per ogni arco, nel range tra 1 e 10, e le domande per ogni nodo, assicurandoci che almeno un nodo abbia domanda positiva
(e che il totale della domanda positiva sia maggiore di 15) ed almeno un altro nodo abbia domanda negativa (e che il totale della domanda negativa sia pari
a quello della domanda positiva).
Inoltre generiamo i costi per ogni arco nel grafo come numeri tra 1 ed 10.
"""

import numpy as np
import gurobipy as gp
from gurobipy import GRB


np.random.seed(1234)

""" Generazione del grafo"""
n_nodes = 200
adj_mat = np.random.rand(n_nodes, n_nodes)
adj_mat[adj_mat > 0.02] = 0
adj_mat *=500
np.fill_diagonal(adj_mat, 0)

b = np.zeros(n_nodes)
b[0]=15
b[100] = -15

c = np.random.rand(n_nodes, n_nodes)*10+0.1
c[c>10] = 10
c[(c<1) * (c>0)] = 10
c[adj_mat==0] = 0
c = c.astype(np.int64)

""" Definizione del modello"""

m = gp.Model('Flusso a costo minimo')

var_idxs = np.nonzero(adj_mat)

var_idxs = [(i,j) for i, j in zip(var_idxs[0], var_idxs[1])]

cost = {idx: c[idx] for idx in var_idxs}
capacity = {idx: adj_mat[idx] for idx in var_idxs}

arcs = m.addVars(var_idxs, lb = 0, ub = capacity, obj = cost, name = 'x')

m.addConstrs(arcs.sum(v, '*')-arcs.sum('*',v) == b[v] for v in range(n_nodes))

m.optimize()






