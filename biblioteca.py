"""
Un bibliotecario deve decidere quali libri acquistare per la biblioteca. I libri sono divisi in quattro categorie diverse
in base all'argomento e alla dimensione: Romanzi brevi, Romanzi lunghi, Manuali brevi, e Manuali lunghi. Ogni volume ha
rispettivamente un costo di 5, 8, 7, 3 euro e uno spessore di 2, 4, 3, 5 cm. Sapendo che normalmente le preferenze per
queste categorie assumono rispettivamente i valori 4, 3, 5, 6, l'obiettivo è di effettuare gli acquisti in modo da
massimizzare il gradimento complessivo sapendo di avere a disposizione un budget di 300 euro.
Tutti i libri devono essere riposti in uno scaffale della lunghezza di 180 cm. Inoltre deve essere acquistato un numero
minimo di romanzi (12) e di manuali (10).
Infine
• il numero di romanzi brevi deve essere uguale al doppio del numero di manuali brevi.
• La somma di romanzi brevi e manuali lunghi deve essere almeno il doppio della somma di romanzi lunghi e manuali brevi.
• la spesa per romanzi lunghi non può essere inferiore al 25% della spesa complessiva.
"""

import gurobipy as gp
from gurobipy import GRB

libri = ['Romanzi brevi', 'Romanzi lunghi', 'Manuali brevi', 'Manuali lunghi']

costi = {
    'Romanzi brevi': 5,
    'Romanzi lunghi': 8,
    'Manuali brevi': 7,
    'Manuali lunghi': 3
}

spessori = {
    'Romanzi brevi': 2,
    'Romanzi lunghi': 4,
    'Manuali brevi': 3,
    'Manuali lunghi': 5
}

preferenze = {
    'Romanzi brevi': 4,
    'Romanzi lunghi': 3,
    'Manuali brevi': 5,
    'Manuali lunghi': 6
}

budget = 300

m = gp.Model('Biblioteca')

x = m.addVars(libri, lb = 0, vtype = GRB.INTEGER, name = 'x')

m.setObjective(gp.quicksum(x[i]*preferenze[i] for i in libri), GRB.MAXIMIZE)

m.addConstr(gp.quicksum(x[i]*costi[i] for i in libri) <= budget)

m.addConstr(gp.quicksum(x[i]*spessori[i] for i in libri) <= 180)

m.addConstr(x['Romanzi brevi']+x['Romanzi lunghi'] >= 12)

m.addConstr(x['Manuali brevi']+x['Manuali lunghi'] >= 10)

m.addConstr(x['Romanzi brevi']== 2*x['Manuali brevi'])

m.addConstr(x['Romanzi brevi'] + x['Manuali lunghi'] >= 2*(x['Romanzi lunghi'] + x['Manuali brevi']))

m.addConstr(x['Romanzi lunghi']*costi['Romanzi lunghi'] >= 0.25*(gp.quicksum(x[i]*costi[i] for i in libri)))

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    for i in libri:
        print(f"x[{i}] = {x[i].X} volti")
    print(f"\nCosto totale: {m.ObjVal} €")