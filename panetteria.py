"""
La panetteria La Spiga d'Oro prepara e vende panettoni, pizza bianca e ciambellone per i clienti del suo forno.
1 kg di panettone richiede, tra gli altri ingredienti, 700 g di pasta lievitata, 2 uova e 200 g di zucchero;
per produrre 1 kg di pizza bianca occorre 1 kg di pasta lievitata. Ogni chilogrammo di ciambellone richiede,
tra gli altri ingredienti, 500 g di farina, 4 uova e 300 g di zucchero. Per preparare 1 kg di pasta lievitata
occorre mescolare 600 g di farina, 50 g di zucchero e 20 g di lievito di birra, oltre a 350 g di acqua 50 g di sale.
Lo scorso 6 dicembre in magazzino le scorte di prodotti ammontavano a 15 kg di farina, 200 g di lievito di birra,
32 uova e 6 kg di zucchero. Quale sarebbe dovuto essere il piano di produzione ottimale per massimizzare l'incasso del
giorno successivo, considerando che panettoni, pizza bianca e ciambellone vengono venduti, rispettivamente
a 7 €, 6 € e 10 € euro al chilogrammo. Inoltre, si sa che la panetteria ha già ricevuto un ordine per 4kg di pizza bianca,
solitamente non vengono venduti più di 7kg di panettone in una giornata e che, per motivi di inventario,
la quantità di farina disponibile a magazzino deve sempre essere almeno il doppio di quella di zucchero.
"""

import gurobipy as gp
from gurobipy import GRB

prodotti = ['Panettone', 'Pizza bianca', 'Ciambellone']

prodotti_extra = ['Pasta lievitata']

ingredienti = ['Farina', 'Lievito di birra', 'Uova', 'Zucchero', 'Acqua', 'Sale']


qt_ingredienti = {
    'Panettone': {'Farina': (600*1000)/700, 'Lievito di birra': 20, 'Uova': 2, 'Zucchero': 200+(50*1000)/700, 'Acqua': 50, 'Sale': 50},
    'Pizza bianca': {'Farina': 600, 'Lievito di birra': 20, 'Uova': 0, 'Zucchero': 50, 'Acqua': 50, 'Sale': 50},
    'Ciambellone': {'Farina': 500, 'Lievito di birra': 0, 'Uova': 4, 'Zucchero': 300, 'Acqua': 0, 'Sale': 0}
}

scorte = {
    'Farina': 15000,
    'Lievito di birra': 200,
    'Uova': 32,
    'Zucchero': 6000,
    'Acqua': float('inf'),
    'Sale': float('inf')
}

prezzi = {
    'Panettone': 7,
    'Pizza bianca': 6,
    'Ciambellone': 10
}

m = gp.Model('Panetteria')

x = m.addVars(prodotti, lb = 0, vtype = GRB.CONTINUOUS, name = 'x')


m.addConstrs(gp.quicksum(x[i]*qt_ingredienti[i][j] for i in prodotti) <= scorte[j] for j in scorte)

m.addConstr(x['Pizza bianca'] >= 4)
m.addConstr(x['Panettone'] <= 7)

m.setObjective(gp.quicksum(x[i]*prezzi[i] for i in prodotti), GRB.MAXIMIZE)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\n Soluzione ottima trovata: \n")
    for i in prodotti:
        print(f"x[{i}] = {x[i].X}")
    print(f"\n Incasso totoale: {m.ObjVal} € \n")

