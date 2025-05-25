"""
Un investitore desidera ottimizzare un portafoglio composto da cinque diverse classi di attività finanziarie: azioni,
obbligazioni, immobili, materie prime e titoli del mercato monetario. Supponendo che la somma delle percentuali
investite nelle cinque classi di attività deve essere pari al 100% del capitale e il rendimento atteso per ogni attività
è pari rispettivamente a 1.2, 1.5, 1.8, 1.05, 1.13, l'obiettivo è massimizzare il rendimento atteso del portafoglio,
rispettando una serie di vincoli relativi al rischio, alla diversificazione e alle esigenze di liquidità.
Infatti, almeno il 25% del portafoglio deve essere investita in titoli del mercato monetario, per garantire
la disponibilità di fondi a breve termine.
Inoltre per evitare un'eccessiva concentrazione in una singola classe di attività, ogni investimento non può superare
il 35% del portafoglio totale.
Si osservi poi che per ridurre il rischio di mercato specifico di una regione, almeno il 40% del portafoglio deve essere
investito in attività diversificate quali le obbligazioni e le materie prime.
Infine il rischio totale del portafoglio, misurato come una combinazione ponderata della deviazione standard
dei rendimenti, non deve superare un valore massimo accettabile pari a 21, dove (12, 23, 31, 9, 18) sono le
deviazioni standard dei singoli rendimenti.
"""

import gurobipy as gp
from gurobipy import GRB

assets = ['Azioni', 'Obbligazioni', 'Immobili', 'Materie prime', 'Titoli del mercato monetario']

rendimenti = {
    'Azioni': 1.2,
    'Obbligazioni': 1.5,
    'Immobili': 1.8,
    'Materie prime': 1.05,
    'Titoli del mercato monetario': 1.13
              }
deviazioni = {
    'Azioni': 12,
    'Obbligazioni': 23,
    'Immobili': 31,
    'Materie prime': 9,
    'Titoli del mercato monetario': 18
}

m = gp.Model('Investimenti')

x = m.addVars(assets, lb=0, vtype=GRB.CONTINUOUS, name='x')

m.addConstr(gp.quicksum(x[i] for i in assets)*0.25 <= x['Titoli del mercato monetario'] )

m.addConstrs(gp.quicksum(x[i] for i in assets)*0.35 >= x[i] for i in assets)

m.addConstr(gp.quicksum(x[i] for i in assets)*0.40 <= x['Obbligazioni'] + x['Materie prime'])

m.addConstr(gp.quicksum(x[i]*deviazioni[i] for i in assets) <= 21)

m.addConstr(gp.quicksum(x[i] for i in assets) == 1) # percentuale totale = 100%

m.setObjective(gp.quicksum(rendimenti[i]*x[i] for i in assets), GRB.MAXIMIZE)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    for i in assets:
        print(f"x[{i}] = {x[i].X} %")
    print(f"\nRendimento totale del portafoglio: {m.ObjVal:.2f} %")
