"""
 La Childfair Company ha tre stabilimenti per la produzione di carrozzine per bambini che devono essere spedite a
 quattro centri di distribuzione. Gli stabilimenti 1, 2 e 3 generano rispettivamente 12, 17 e 11 spedizioni mensili.
 Ogni centro di distribuzione deve ricevere 1O spedizioni al mese. La distanza fra ogni
stabilimento e i rispettivi centri di distribuzione è indicata a destra
stabilimenti            centri
            1      2        3       4
        1  800km  1300km  400km  700km
        2  1100km  1400km  600km  1000km
        3  600km  1200km  800km  900km

Il costo del trasporto per ogni spedizione è di 100 euro più 50 centesimi per km.
Quanto dovrebbe essere spedito da ogni stabilimento a ciascuno dei centri di
distribuzione così da minimizzare il costo totale di trasporto?
(a) Formulare questo problema come problema di trasporto costruendo l'opportuna tabella dei parametri.
(b) Disegnare la rappresentazione su rete di questo problema.
(c) Determinare una soluzione ottima.
"""

import gurobipy as gp
from gurobipy import GRB

stabilimenti = list(range(3))
centri = list(range(4))

spedizione = [12, 17, 11]
req = [10, 10, 10, 10]

costo_fisso = 100
costo_km = 50

km = [[800, 1300, 400, 700],
      [1100, 1400, 600, 1000],
      [600, 1200, 800, 900]]

m = gp.Model('ChildfairCompany')

x = m.addVars(stabilimenti, centri, lb=0, vtype=GRB.INTEGER, name='x')

m.setObjective(gp.quicksum(costo_fisso + x[i,j]*costo_km*km[i][j] for i in stabilimenti for j in centri), GRB.MINIMIZE)

m.addConstrs(gp.quicksum(x[i,j] for i in stabilimenti) == req[j] for j in centri)

m.addConstrs(gp.quicksum(x[i, j] for j in centri) <= spedizione[i] for i in stabilimenti)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\n Soluzione ottima trovata: \n")
    for i in stabilimenti:
        for j in centri:
            if x[i, j].X > 0.5:
                print(f"Da stabilimento {i+1} {x[i,j].X} spedizioni verso centro {j+1}")
    print(f"\n Costo totale: {m.ObjVal} euro")
