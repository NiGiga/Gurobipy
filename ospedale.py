"""
Un’azienda ospedaliera deve riorganizzare i turni del personale che sorveglia la struttura. Ogni sorvegliante,
indipendentemente dalla collocazione all’interno della settimana, lavora 5 giorni consecutivi e poi ha diritto a due giorni
di riposo. Le esigenze di servizio per i vari giorni della settimana richiedono la presenza del seguente numero minimo
di addetti alla sicurezza:

    Giorno|----|Numero Minimo
    Lunedi|----------|28
    Martedi|---------|18
    Mercoledi|-------|20
    Giovedi|---------|26
    Venerdi|---------|22
    Sabato|----------|13
    Domenica|--------|13

Ciascun dipendente viene retribuito in base al giorno della settimana in cui lavora. In particolare il costo che l’ospedale
sostiene per retribuire un addetto alla sicurezza è di 50 euro al giorno
(per i turni del lunedì, martedì, mercoledì, giovedì e venerdì), di 75 euro al giorno per i turni di sabato
e di 85 euro al giorno per i turni di domenica. Ad esempio, un addetto alla sicurezza il cui turno comincia il giovedì,
per i suoi 5 giorni lavorativi (dal giovedì al lunedì) riceve una retribuzione pari a euro 310 (ovvero 50 × 3 + 75 + 85).
Obiettivo dell’azienda ospedaliera è quello di minimizzare i costi complessivi settimanali di retribuzione della sorveglianza.
a) Si determini il piano dei turni di lavoro ottimale per minimizzare il costo settimanale per l’ospedale.
b) A seguito di una richiesta sindacale l’ospedale deve garantire che nella retribuzione degli addetti alla sorveglianza
non vi sia una differenza superiore ai 40 euro. Si determini nuovamente il piano dei turni di lavoro considerando questo
ulteriore vincolo.
"""

import gurobipy as gp
from gurobipy import GRB

giorni = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica']
n = len(giorni)
N = 50  # numero totale di lavoratori
lavoratori = range(N)

num_min_adetti = {
    'Lunedi': 28,
    'Martedi': 18,
    'Mercoledi': 20,
    'Giovedi': 26,
    'Venerdi': 22,
    'Sabato': 13,
    'Domenica': 13
}

costo = {
    'Lunedi': 50,
    'Martedi': 50,
    'Mercoledi': 50,
    'Giovedi': 50,
    'Venerdi': 50,
    'Sabato': 75,
    'Domenica': 85
}

m = gp.Model('Ospedale')

x = m.addVars(lavoratori, giorni, vtype=GRB.BINARY, name='x')

m.addConstrs(gp.quicksum(x[i,j] for i in lavoratori) >= num_min_adetti[j] for j in giorni)

giorni_idx = {giorni[i]: i for i in range(n)}
for l in lavoratori:
    for i in range(n - 6):  # intervalli di 7 giorni
        g5 = giorni[i:i+5]
        g2 = giorni[i+5:i+7]
        m.addConstr(gp.quicksum(x[l, g] for g in g5) <= 3 + gp.quicksum(1 - x[l, g] for g in g2))

m.setObjective(gp.quicksum(x[i,j]*costo[j] for i in lavoratori for j in costo), GRB.MINIMIZE)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    for i in lavoratori:
        for j in giorni:
            print(f"x[{i},{j}] = {x[i,j].X}")

    for j in giorni:
        totale = sum(x[i, j].X for i in lavoratori)
        print(f"{j}: {int(totale)} lavoratori assegnati")

    print(f"\nCosto totale: {m.ObjVal:.2f} euro")