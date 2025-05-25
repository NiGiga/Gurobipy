"""
Un industria calzaturiera produce 3 diversi modelli di scarpe (A, B e C) in 5 stabilimenti dislocati nel territorio. Le calzature
vengono vendute al prezzo di 30, 55 e 40 euro rispettivamente. Dovendo decidere il piano produttivo per il mese seguente, il gruppo
industriale deve decidere quali materie prime acquistare e come gestire la produzione per massimizzare il proprio profitto.

Per l’acquisto di materie prime, l’azienda ha a disposizione 1000 euro e puo’ acquistare pelle al prezzo di 4.5 euro/mq, lacci al prezzo
di 73 cent/mt e suole al prezzo di 7 euro/unita’.

In un mese gli stabilimenti posso produrre le seguenti quantita di scapre (in paia):

| Modello| Stabilimento 1 | Stabilimento 2 | Stabilimento 3 | Stabilimento 4 | Stabilimento 5 |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| A | 4 | 12 | 3 | 9 | 7 |
| B | 2 | 7 | 3 | 14 | 5 |
| C | 8 | 3 | 5 | 2 | 9 |


La produzione di una calzatura richiede una suola per tutti I modelli di scapre,
ed in oltre: 1mq di pelle e 50cm di lacci per il modello A, 0.7mq di pelle e 45cm di lacci per il modello B, 1.35mq di pelle
e 90cm di lacci per il modello C.

Considerando che le materie prime acquistate posso essere distribuite agli stabilimenti produttivi in tagli da 10mq di pelle,
5mt di lacci e blocchi di 3 paia di suole. Si determini l’approvvigionamento del gruppo industriale, la distribuzione delle materie prime
e la produzione in paia dei singoli stabilimenti in modo tale da massimizzare il profitto del gruppo, asssumendo che tutta la produzione venga venduta
e sapendo ulteriormente che:

1. Devono essere prodotte almeno 5 paia di scarpe di tipo A

2. La produzione in paia dello stabilimento 3 deve essere pari a quella dello stabilimento 1

3. Lo stabilimento 4 ha gia’ ricevuto una commessa per 2 paia di scarpe di tipo B
"""

import gurobipy as gp
from gurobipy import GRB


m = gp.Model('Scarpe')

scarpe = ['A', 'B', 'C']
stabilimenti = ['1', '2', '3', '4', '5']

prezzi_vendita = {'A': 30, 'B': 55, 'C': 40}

costo_pelle = 4.5
costo_lacci = 0.73
costo_suole = 7

budget = 1000

richiesta_pelle = {'A': 1, 'B': 0.7, 'C': 1.35}
richiesta_lacci = {'A': 0.5, 'B': 0.45, 'C': 0.9}
richiesta_suole = {'A': 1, 'B': 1, 'C': 1}

blocco_pelle = 10
blocco_lacci = 5
blocco_suole = 3

# Capacità produttive per ogni scarpe e per ogni stabilimento
cap = {
    ('A', '1'): 4, ('A', '2'): 12, ('A', '3'): 3, ('A', '4'): 9, ('A', '5'): 7,
    ('B', '1'): 2, ('B', '2'): 7, ('B', '3'): 3, ('B', '4'): 14, ('B', '5'): 5,
    ('C', '1'): 8, ('C', '2'): 3, ('C', '3'): 5, ('C', '4'): 2, ('C', '5'): 9
}

# Decision variables: quantità di scarpe di tipo i per stabilimento j
x = m.addVars(scarpe,stabilimenti, lb=0, vtype=GRB.INTEGER, name="x")

# Decision variables: quantità di pelle, lacci e suole
qp = m.addVar(vtype=GRB.INTEGER, name="qt pelle")
qs = m.addVar(vtype=GRB.INTEGER, name="qt suole")
ql = m.addVar(vtype=GRB.INTEGER, name="qt lacci")

# Decision variables: quantità di blocchi di pelle, lacci e suole
p = m.addVars(stabilimenti, vtype=GRB.INTEGER, name="blocchi pelle")
s = m.addVars(stabilimenti, vtype=GRB.INTEGER, name="blocchi suole")
l = m.addVars(stabilimenti, vtype=GRB.INTEGER, name="blocchi lacci")

# Constrain: quantità di scarpe di tipo i per stabilimento j
m.addConstr((qp*costo_pelle*blocco_pelle + qs*costo_suole*blocco_suole + ql*costo_lacci*blocco_lacci) <= budget, name="limite budget")

# Constrain: quantità di scarpe di tipo i per stabilimento j
for j in stabilimenti:
    m.addConstr(gp.quicksum(x[i,j]*richiesta_pelle[i] for i in scarpe) <= qp*blocco_pelle , name="pelle")
    m.addConstr(gp.quicksum(x[i,j]*richiesta_suole[i] for i in scarpe) <= qs*blocco_suole, name="suole")
    m.addConstr(gp.quicksum(x[i,j]*richiesta_lacci[i] for i in scarpe) <= ql*blocco_lacci, name="lacci")

# Constrain: capacità produttiva per ogni scarpe e per ogni stabilimento
for i in scarpe:
    for j in stabilimenti:
        m.addConstr(x[i,j] <= cap[i,j], name="capacita")

# Constrain: minimo scarpe di tipo A
m.addConstr(gp.quicksum(x['A',j] for j in stabilimenti) >= 5, name="minimo scarpe")

# Constrain: quantità di scarpe di tipo A per stabilimento 3 = quantità di scarpe di tipo 1 per stabilimento 3
m.addConstr(gp.quicksum(x[i,'3'] for i in scarpe) == gp.quicksum(x[i,'1'] for i in scarpe), name="produzione stabilimenti")

# Constrain: quantità di scarpe di tipo B per stabilimento 4
m.addConstr(x['B','4'] >= 2, name="produzione stabilimenti")

# Objective function: maximizzare il profitto
m.setObjective(gp.quicksum(x[i,j]*prezzi_vendita[i] for i in scarpe for j in stabilimenti)
               -(qp*costo_pelle*blocco_pelle + qs*costo_suole*blocco_suole + ql*costo_lacci*blocco_lacci),GRB.MAXIMIZE)

m.optimize()

# Output solution if optimal
if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    for i in scarpe:
        for j in stabilimenti:
            print(f"x[{i},{j}] = {x[i,j].X}")
    print(f"\nCosto totale: {m.ObjVal:.2f} €")
    print(f"\nQuantità di pelle: {qp.X:.2f} mq")
    print(f"\nQuantità di suole: {qs.X:.2f} unita'")
    print(f"\nQuantità di lacci: {ql.X:.2f} cm")
    print(f"\nQuantità di blocchi di pelle: {qp.X*blocco_pelle:.2f} paia")