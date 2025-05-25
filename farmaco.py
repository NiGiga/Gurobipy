# Esercizio 3 – Ottimizzazione di un trattamento farmacologico

# Un paziente deve assumere una sostanza X durante il giorno, usando due tipi di farmaci: Prismil e Cilindren.
# La giornata è divisa in 8 fasce orarie da 3 ore ciascuna.
# In ogni fascia, il paziente può assumere entrambi i farmaci.

# L'effetto dei farmaci è misurato dal tasso di una proteina Y nel sangue, proporzionale alla quantità
# di sostanza X assunta, indipendentemente dal tipo di farmaco.

# La somma degli effetti nelle varie fasce orarie si somma.
# L’assunzione ha lo scopo di mantenere il tasso di proteina Y >= ad un certo minimo fisiologico,
# che varia a seconda della fascia oraria e dipende dall’attività dell’organismo (vedi Tabella 1).

# Tabella 1: Valori minimi di proteina Y (mg/cc) da assicurare per ciascuna fascia oraria (3 ore):
#   0:00 - 3:00  →  2.5
#   3:00 - 6:00  →  0.0
#   6:00 - 9:00  → 11.0
#   9:00 - 12:00 →  4.0
#   12:00 - 15:00 → 27.0
#   15:00 - 18:00 →  8.0
#   18:00 - 21:00 → 20.0
#   21:00 - 24:00 → 15.0

# Il livello massimo consentito di proteina Y è 45 mg/cc.

# Ogni farmaco ha un effetto temporale diverso: per ogni quantità somministrata, l’effetto varia
# in base alle ore trascorse dall’assunzione. (Tabella 2)

# Tabella 2: Effetto (mg/cc) di 1 grammo di farmaco a seconda del tempo trascorso dall’assunzione:
# Righe: Ore trascorse dall’assunzione (0–3, 3–6, 6–9, 9–12, 12+)
# Colonne: Farmaci Prismil e Cilindren

# | Ore trascorse | Prismil | Cilindren |
# |---------------|---------|-----------|
# | 0 – 3         | 2.8     | 3.0       |
# | 3 – 6         | 1.9     | 2.7       |
# | 6 – 9         | 0.7     | 0.3       |
# | 9 – 12        | 0.0     | 0.0       |
# | 12 o più      | 0.0     | 0.0       |

# Obiettivo: Trovare la quantità di ciascun farmaco da somministrare in ogni fascia oraria
# in modo che il livello minimo di proteina Y sia rispettato in ogni fascia oraria,
# senza superare il limite massimo (45 mg/cc), e minimizzando il costo complessivo.

# Costi:
# - Prismil: 0.70 Euro/grammo
# - Cilindren: 0.95 Euro/grammo

# Variabili: x[i,j] = quantità di farmaco i (Prismil o Cilindren) somministrata nella fascia oraria j

# L’obiettivo è costruire un modello di ottimizzazione lineare per determinare le quantità minime
# da somministrare rispettando tutti i vincoli.

import gurobipy as gp
from gurobipy import GRB

m = gp.Model('Farmaco')

farmaci = ['Prismil', 'Cilindren']

fasce = list(range(8))

min_proteina = [2.5, 0.0, 11.0, 4.0, 27.0, 8.0, 20.0, 15.0]

max_proteina = 45.0

effetto = {
    'Prismil': [2.8, 1.9, 0.7, 0.0, 0.0],
    'Cilindren': [3.0, 2.7, 0.3, 0.0, 0.0]
}

costi = {'Prismil': 0.7, 'Cilindren': 0.95}

x = m.addVars(farmaci, fasce, lb=0, vtype=GRB.CONTINUOUS, name='x')

for t in fasce:
    effetto_tot = gp.quicksum(x[i,j]*effetto[i][t-j] for i in farmaci for j in fasce if 0<= t-j <= 4)
    m.addConstr(effetto_tot <= max_proteina, name=f'Effetto totale {t}')
    m.addConstr(effetto_tot >= min_proteina[t], name=f'Effetto totale {t}')

m.setObjective(gp.quicksum(x[i,j]*costi[i] for i in farmaci for j in fasce), GRB.MINIMIZE)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    for i in farmaci:
        for j in fasce:
            print(f"x[{i},{j}] = {x[i,j].X:.2f} g")
    print(f"\nCosto totale: {m.ObjVal:.2f} €")