"""
La Versatech Corporation ha deciso di produrre tre nuovi prodotti. Cinque gruppi di stabilimenti hanno adesso
un eccesso di capacità produttiva. Il costo unitario di produzione del primo
prodotto è pari a 31, 29, 32, 28 e 29 negli stabilimenti 1, 2, 3, 4 e 5.
Il costo unitario di produzione del secondo prodotto è rispettivamente
di 45, 41, 46, 42 e 43 negli stabilimenti 1, 2, 3, 4 e 5.
Il costo unitario di produzione del terzo prodotto è pari a 38, 35 e 40 negli stabilimenti 1, 2 e 3,
mentre gli stabilimenti 4 e 5 non sono in grado di produrre questo prodotto. Le previsioni di vendita indicano
che dovrebbero essere prodotti rispettivamente 600, 1000 e 800 unità dei prodotti 1, 2 e 3 al giorno.
Gli stabilimenti 1, 2, 3, 4 e 5 sono in grado di produrne 400, 600, 400, 600 e 1000 unità giornaliere,
indipendentemente dal prodotto o dalla combinazione di prodotti in questione. Si assuma che ogni stabilimento
che ha la possibilità e la capacità di produrre certi prodotti possa produrli in qualunque combinazione e in
qualsiasi quantità.
Il management desidera conoscere come allocare i nuovi prodotti agli stabilimenti per minimizzare il costo totale di produzione.
(a) Formulare questo problema come problema di trasporto costruendo l'opportuna tabella dei parametri.
(b) Determinare una soluzione ottima.
"""

import gurobipy as gp
from gurobipy import GRB

prodotti = list(range(3))
stabilimenti = list(range(5))

costi = [[31, 29, 32, 28, 29],
         [45, 41, 46, 42, 43],
         [38, 35, 40, 1000, 1000]]

req_prod = [600, 1000, 800]

limite_stabilimenti = [400, 600, 400, 600, 1000]

m = gp.Model('VarsatechCorp')

x = m.addVars(prodotti, stabilimenti, lb=0, vtype=GRB.INTEGER, name='x')

m.setObjective(gp.quicksum(costi[i][j]*x[i, j] for i in prodotti for j in stabilimenti), GRB.MINIMIZE)

m.addConstrs(gp.quicksum(x[i, j] for i in stabilimenti) >= req_prod[j] for j in prodotti)

m.addConstrs(gp.quicksum(x[i, j] for i in prodotti) <= limite_stabilimenti[j] for j in stabilimenti)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\n Soluzione ottima trovata: \n")
    for i in prodotti:
        for j in stabilimenti:
            if x[i, j].X > 0.5:
                print(f"Da prodotto {i+1} {x[i,j].X} unità verso stabilimento {j+1}")
    print(f"\n Costo totale: {m.ObjVal} euro")