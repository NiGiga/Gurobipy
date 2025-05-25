"""
Un impianto che produce lavatrici deve pianificare la produzione per i prossimi 5 mesi. La quantità rimasta
invenduta al termine di ogni mese resta in magazzino ed è disponibile per essere venduta nel mese successivo.
Tuttavia, per ogni unità rimasta invenduta si sostiene un costo di 10 euro/pezzo per ogni mese di giacenza.
L’impianto ha una capacità produttiva di 110 pezzi al mese ad un costo di 300 euro al pezzo.
E’ però possibile produrre ulteriori 60 pezzi al mese al costo di 330 euro al pezzo. Sapendo che la domanda
per i prossimi 5 mesi è stimata in 100, 130, 150, 140, e 180 pezzi rispettivamente, si vuole pianificare la produzione
in ciascun mese in modo da minimizzare i costi complessivi.

NOTA:
forall mese t = 1,..,5

x_t := qt prodotta al costo normale
y_t := qt prodotta con costo extra
s_t := qt rimasta in magazzino (invenduta a fine mese)
d_t := domanda per il mese t
s_0 := qt iniziale in magazzino (in questo caso 0)

EQ di bilancio:
x_t + y_t + s_(t-1) = d_t + s_t

OBJ:

max sum_(t=1, 5) (300x_t + 330y_t + 10s_t

"""
import gurobipy as gp
from gurobipy import GRB

m = gp.Model('Lavatrici')

mesi = ['Mese 1', 'Mese 2', 'Mese 3', 'Mese 4', 'Mese 5']

costo_invenduta = 10

costo_prodotto = 300
costo_prodotto_extra = 330

cap_mese = 110
cap_extra = 60

domanda ={
    'Mese 1': 100,
    'Mese 2': 130,
    'Mese 3': 150,
    'Mese 4': 140,
    'Mese 5': 180
}

x = m.addVars(mesi, lb=0, vtype=GRB.INTEGER, name='x')
y = m.addVars(mesi, lb=0, vtype=GRB.INTEGER, name='y')
s = m.addVars(mesi, lb=0, vtype=GRB.INTEGER, name='s')

for i in mesi:
    m.addConstr(x[i] <= cap_mese)
    m.addConstr(y[i] <= cap_extra)

s_pre = 0
for i in mesi:
    m.addConstr(x[i] + y[i] + s_pre == domanda[i] + s[i])
    s_pre = s[i]

m.addConstrs(x[i] + y[i] + s[i] >= domanda[i] for i in mesi)

m.setObjective(gp.quicksum(300*x[i] + 330*y[i] + 10*s[i] for i in mesi), GRB.MINIMIZE)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    for i in mesi:
        print(f"Mese {i}: \n")
        print(f"Numero pezzi produzione standard: {x[i].X}")
        print(f"Numero pezzi produzione extra: {y[i].X} pezzi")
        print(f"Numero pezzi invenduti: {s[i].X} pezzi \n")

    print(f"\n Costo totale: {m.ObjVal:.2f} €")
