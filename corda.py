"""
Esercizio 2
Un’azienda produce corde in spezzoni da 100 m che devono essere tagliati in due parti. A loro volta, i due spezzoni
cosi ottenuti andranno avvolti, rispettivamente, su un quadrato e su un triangolo isoscele. L’azienda vuole determinare
come tagliare lo spezzone di cor-da affinche’ si minimizzi la somma dei perimetri delle due forme utilizzate per
avvolgere gli spezzoni di corda. Inoltre, l’azienda vuole che lo spezzone di corda che verra’ avvolto sul quadrato non
faccia piu’ di 5 giri e che quello che verra’ avvolto sul triangolo non ne faccia piu’ di 4. Determinare la lunghezza
degli spezzoni di corda da tagliare e il lato del quadrato e del triangolo sapendo che la base di quest’ultimo e’
fissata a 2 e che entrambi i lati devono avere lunghezza almeno pari ad 1
"""

import gurobipy as gp
from gurobipy import GRB

corda_totale = 100  # lunghezza totale della corda in metri

# Creazione del modello
m = gp.Model('Esercizio 2')

# Variabili decisionali
lato_quadrato = m.addVar(lb=1, vtype=GRB.CONTINUOUS, name='lato_quadrato')
lato_triangolo = m.addVar(lb=1, vtype=GRB.CONTINUOUS, name='lato_triangolo')
lunghezza_corda_quadrato = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name='lunghezza_corda_quadrato')
lunghezza_corda_triangolo = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name='lunghezza_corda_triangolo')

# Perimetri delle forme
perimetro_quadrato = 4 * lato_quadrato
base_triangolo = 2  # base fissa del triangolo isoscele
perimetro_triangolo = base_triangolo + 2 * lato_triangolo

# Funzione obiettivo: minimizzare la somma dei perimetri
m.setObjective(perimetro_quadrato + perimetro_triangolo, GRB.MINIMIZE)

# Vincolo sulla lunghezza totale della corda
m.addConstr(lunghezza_corda_quadrato + lunghezza_corda_triangolo == corda_totale, "vincolo_lunghezza_totale")

# Vincoli sul numero di giri
# Il quadrato non può fare più di 5 giri
m.addConstr(lunghezza_corda_quadrato <= 5 * perimetro_quadrato, "vincolo_giri_quadrato")
# Il triangolo non può fare più di 4 giri
m.addConstr(lunghezza_corda_triangolo <= 4 * perimetro_triangolo, "vincolo_giri_triangolo")

# Vincoli sulla lunghezza minima della corda per ogni forma
# La corda deve fare almeno un giro completo
m.addConstr(lunghezza_corda_quadrato >= perimetro_quadrato, "vincolo_min_giri_quadrato")
m.addConstr(lunghezza_corda_triangolo >= perimetro_triangolo, "vincolo_min_giri_triangolo")

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    print(f"Lato del quadrato: {lato_quadrato.X:.2f} m")
    print(f"Lato del triangolo isoscele: {lato_triangolo.X:.2f} m")
    print(f"Base del triangolo isoscele: {base_triangolo:.2f} m")
    print(f"\nLunghezza corda per il quadrato: {lunghezza_corda_quadrato.X:.2f} m")
    print(f"Lunghezza corda per il triangolo: {lunghezza_corda_triangolo.X:.2f} m")
    print(f"\nPerimetro del quadrato: {lato_quadrato.X*4:.2f} m")
    print(f"Perimetro del triangolo: {lato_triangolo.X*2 + base_triangolo :.2f} m")
    print(f"Somma dei perimetri (valore ottimale): {m.ObjVal:.2f} m")

    # Calcolo del numero di giri
    giri_quadrato = lunghezza_corda_quadrato.X / (lato_quadrato.X*4)
    giri_triangolo = lunghezza_corda_triangolo.X / (lato_triangolo.X*2 + base_triangolo)
    print(f"\nNumero di giri sul quadrato: {giri_quadrato:.2f}")
    print(f"Numero di giri sul triangolo: {giri_triangolo:.2f}")
