"""
Un allenatore sta pianificando il programma di allenamento di una squadra di basket per il mese successivo.
L'obiettivo è massimizzare i livelli di forma fisica complessiva dei giocatori, rispettando i vincoli di tempo,
garantendo sessioni di allenamento equilibrate e soddisfacendo le esigenze di recupero. Infatti ogni settimana ci
sono delle sessioni dedicate all'allenamento di resistenza, all’allenamento della forza e ad esercitazioni di
abilità. In particolare, la squadra ha a disposizione un massimo di 20 ore settimanali per l’allenamento; deve
dedicare almeno 4 ore alla settimana all'allenamento di resistenza per mantenere la forma cardiovascolare; per
garantire uno sviluppo equilibrato, le ore dedicate all'allenamento della forza dovrebbero essere almeno la
metà di quelle dedicate alle esercitazioni sulle abilità; la squadra non dovrebbe dedicare più di 8 ore a
settimana all'allenamento della forza per evitare il sovrallenamento e gli infortuni, il totale delle ore dedicate
all'allenamento di resistenza e alle esercitazioni di abilità non deve superare le 18 ore settimanali, per garantire
un tempo adeguato per altre attività e per il recupero. Ogni ora di allenamento di resistenza, forza e abilità,
contribuisce alla forma fisica secondo i coefficienti 5, 4, 6, rispettivamente.
Presentato il piano di allenamento alla squadra, i giocatori richiedono di rivedere il programma e di minimizzare
il numero di ore di allenamento dedicato alla forza, mantenendo lo stesso numero ottimo di ore di allenamento
settimanali. La dirigenza vuole quindi valutare quanto sarebbe la perdita in termini di forma fisica del piano di
allenamento proposto dai giocatori.

NOTA PERSONALE:
Poiché i vincoli e l’obiettivo sono tutti formulati su base settimanale e il programma si ripete ogni settimana
per 4 settimane, è sufficiente modellare e ottimizzare una singola settimana.
"""

import gurobipy as gp
from gurobipy import GRB

m = gp.Model('Basket')

allenamenti = ['Resistenza', 'Forza', 'Abilità']


ore_settimana = 20

coeff = {
    'Resistenza': 5,
    'Forza': 4,
    'Abilità': 6
}

x = m.addVars(allenamenti, lb=0, ub=ore_settimana, vtype=GRB.CONTINUOUS, name='x')

m.addConstr(gp.quicksum(x[i] for i in allenamenti) <= ore_settimana)

m.addConstr(x['Resistenza'] >= 4)

m.addConstr(x['Forza'] >= x['Abilità']/2)

m.addConstr(x['Forza'] <= 8)

m.addConstr(x['Resistenza'] + x['Abilità'] <= 18)

m.setObjective(gp.quicksum(coeff[i]*x[i] for i in allenamenti), GRB.MAXIMIZE)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    for i in allenamenti:
        print(f"x[{i}] = {x[i].X} ore")
    print(f"\nPunteggio forma fisica: {m.ObjVal:.2f} pt")