"""
La BETTER PRODUCTS COMPANY ha deciso di iniziare la produzione di quattro nuovi
prodotti usando tre stabilimenti che attualmente hanno capacità produttiva in eccesso.
I prodotti richiedono uno sforzo di produzione per unità abbastanza simile, e così la capacità pro-
duttiva disponibile negli stabilimenti è misurata dal numero di unità di ogni prodotto che
può essere prodotto in un giorno, come indicato nella colonna destra della Tabella 7.27.
La riga in basso fornisce il tasso di produzione giornaliero richiesto per soddisfare le vendite programmate.
Ogni stabilimento può produrre uno qualunque dei prodotti, tranne lo stabilimento B che non può produrre il prodotto 2.
Tuttavia, i costi unitari di ogni prodotto differiscono da stabilimento a stabilimento, come indicato nella parte
centrale della Tabella 7.27.
Il management ora deve prendere una decisione su come suddividere la produzione dei prodotti fra gli stabilimenti.
Sono disponibili due tipi di opzioni.
Opzione I: è permesso suddividere la produzione: lo stesso prodotto è fabbricato in più di
            uno stabilimento.
Opzione 2: è vietato suddividere la produzione.
        Questa seconda opzione impone un vincolo che può solo aumentare il costo di una soluzione ottima basata sulla
        Tabella 7.27. D'altra parte, il vantaggio chiave dell'opzione 2 è che elimina alcuni costi nascosti associati
        alla suddivisione del prodotto che non sono presenti nella Tabella 7.27, compresi costi aggiuntivi di setup,
        distribuzione e gestione. Di conseguenza, il management desidera che entrambe le opzioni vengano analizzate
        prima di prendere una decisione finale. Per l'opzione 2, il management specifica inoltre che a ogni stabilimento
        dovrebbe essere assegnato almeno uno dei prodotti.

Per ogni singola opzione verrà formulato il modello e risolto, tenendo conto che l'opzione l conduce a un problema di
trasporto e l'opzione 2 conduce a un problema di assegnamento.

Tab 7.27

      0        1        2        3       capacità
---------------------------------------------------
A     41      27       28       24          75
---------------------------------------------------
B     40      29       --       23          75
---------------------------------------------------
C     37      30       27       21          45
---------------------------------------------------
TP    20      30       30       30

"""


import gurobipy as gp
from gurobipy import GRB

m = gp.Model('BettProdCompany')

stabilimenti = list(range(5))
prodotti = ['A', 'B', 'C']

costi = {
    ('A', 0): 41, ('A', 1): 27, ('A', 2): 28, ('A', 3): 24, ('A', 4): 0,
    ('B', 0): 40, ('B', 1): 29, ('B', 2): 10000, ('B', 3): 23, ('B', 4): 0,
    ('C', 0):37, ('C', 1): 30, ('C', 2): 27, ('C', 3): 21, ('C', 4): 0,
}
cap = {
    'A': 75, 'B': 75, 'C': 45
}
produzione_req = {
    0: 20,
    1: 30,
    2: 30,
    3: 30,
    4: 75
}

"""Opzione I
x = m.addVars(prodotti, stabilimenti, lb=0, vtype=GRB.INTEGER, name='x')

m.setObjective(gp.quicksum(costi[i, j]*x[i, j] for i in prodotti for j in stabilimenti), GRB.MINIMIZE)

m.addConstrs(gp.quicksum(x[i, j] for i in prodotti) >= produzione_req[j] for j in stabilimenti)

m.addConstrs(gp.quicksum(x[i, j] for j in stabilimenti) <= cap[i] for i in prodotti)

m.optimize()
"""

"""Opzione 2"""

x = m.addVars(prodotti, stabilimenti, lb=0, vtype=GRB.INTEGER, name='x')

m.setObjective(gp.quicksum(costi[i, j]*x[i, j] for i in prodotti for j in stabilimenti), GRB.MINIMIZE)

m.addConstrs(gp.quicksum(x[i, j] for i in prodotti) >= produzione_req[j] for j in stabilimenti)

m.addConstrs(gp.quicksum(x[i, j] for j in stabilimenti) <= cap[i] for i in prodotti)

m.addConstrs(x[i, j]>= 1 for i in prodotti for j in stabilimenti if i != 'B' and j != 2)

m.optimize()


if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    for i in prodotti:
        for j in stabilimenti:
            print(f"x[{i},{j}] = {x[i, j].X} unità")
    print(f"\nCosto totale: {m.ObjVal} €")
