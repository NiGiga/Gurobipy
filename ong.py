"""
Un'organizzazione umanitaria deve distribuire quattro tipi di risorse - acqua la cui importanza è pari a 4, cibo
(importanza=5), medicinali (importanza=9) e coperte (importanza=3)- in una regione colpita da un disastro
naturale. Ci sono diverse località con differenti livelli di bisogno e condizioni di accesso. L'obiettivo è
massimizzare un punteggio di supporto alle persone, ponderato per l'importanza di ciascuna risorsa tenendo
conto delle risorse limitate, delle condizioni logistiche e delle necessità variabili delle diverse località. In
particolare:
1. Capacità di Trasporto: Le risorse devono essere trasportate da un centro logistico alle località colpite. La
capacità di trasporto totale è limitata a 800 unità, dove acqua, cibo, medicinali e coperte occupano
rispettivamente 1, 3, 2, e 1 unità di spazio.
2. Disponibilità di Risorse: L'organizzazione ha delle riserve limitate. In totale, sono disponibili 300 unità di
acqua, 200 unità di cibo e 150 unità di medicinali, mentre non c'è un limite per le coperte, ma queste
devono essere distribuite in numero almeno pari alla metà di tutte le altre risorse distribuite.
3. Distribuzione Equa: Per garantire un supporto equilibrato, almeno il 40% delle risorse totali distribuite deve
essere rappresentato da acqua e cibo.
4. Limitazioni Logistiche: In alcune località è difficile accedere con molte risorse contemporaneamente. Quindi,
la quantità totale di cibo e medicinali non può superare la somma dell'acqua e delle coperte per garantire
una distribuzione efficace

"""
import gurobipy as gp
from gurobipy import GRB


m = gp.Model('Ong')

risorse = ['Medicinali','Acqua','Coperte', 'Cibo']

importanza = {'Medicinali': 9, 'Acqua': 4, 'Coperte': 3, 'Cibo': 5}
                                                                    # ordinamento proporzionale napsack
pesi = {'Medicinali': 2, 'Acqua': 1, 'Coperte': 1, 'Cibo': 3}

x = m.addVars(risorse, lb=0, vtype=GRB.INTEGER, name='x')

m.addConstr(gp.quicksum(x[i]*pesi[i] for i in risorse) <= 800, name='Capacità di trasporto')

m.addConstrs(x[i] <= (300 if i == 'Acqua' else
                      200 if  i == 'Cibo' else
                      150 if i == 'Medicinali'
                      else float('inf'))
             for i in risorse)

m.addConstr(x['Medicinali']+x['Acqua']+x['Cibo']<= 2*x['Coperte'], name='Distribuzione equa')

m.addConstr(gp.quicksum(x[i] for i in risorse)*0.4 <= x['Acqua']+x['Cibo'])

m.addConstr(x['Cibo'] + x['Medicinali'] <= x['Acqua'] + x['Coperte'], name='Limitazioni logistiche')

m.setObjective(gp.quicksum(x[i]*importanza[i] for i in risorse), GRB.MAXIMIZE)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\n Soluzione ottima trovata: \n")
    for i in risorse:
        print(f"x[{i}] = {x[i].X}")
    print(f"\n Punteggio supporto: {m.ObjVal}")



