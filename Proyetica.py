"""
L’azienda Proyecta lavora con 10 diversi collaboratori esterni che vengono chiamati ed assunti ad ore.
Per portare a termine 5 progetti attualmente aperti, l’azienda vuole affidare gli incarichi rimanenti ai collaboratori
esterni e minimizzare il costo di realizzazione di tutti I progetti.
Avendo le seguenti informazioni, si determini la distribuzione ottimale degli incarichi:
1. Gli incarichi rimanenti in ogni progetto possono essere frazionati liberamente
2. Il numero di ore per cui sono disponibili i collaboratori sono le seguenti: 50, 35, 17, 29, 12, 77, 20, 51, 31, 19.
3. La parcella oraria dei collaboratori sono le seguenti (in euro): 7, 3, 4, 5.2, 2.8, 6, 3.5, 4.9, 3.2, 2.5.
4. Il numero di ore richieste per completare ogni progetto sono: 38, 17, 21, 44, 29.
5. Ai collaboratori 2 e 5, per accordi precedenti, devono essere assegnate un numero di ore tali per cui il compenso
    derivante sia almeno 50 e 25 euro, rispettivamente.
6. Il numero di ore di lavoro assegnate complessivamente ai collaboratori 1, 3, 7 e 9 non deve superare le 70 ore.
7. I collaboratori 4 ed 8 devono essere coinvolti per almeno 5 ore nei progetti 2 e 3, rispettivamente.
"""

import gurobipy as gp
from gurobipy import GRB

collab = list(range(10))
proj = list(range(5))

ore_disp = [50, 35, 17, 29, 12, 77, 20, 51, 31, 19]

costo_ora = [7, 3, 4, 5.2, 2.8, 6, 3.5, 4.9, 3.2, 2.5]

ore_req = [38, 17, 21, 44, 29]

m = gp.Model('Proyetica')

x = m.addVars(proj, collab, lb = 0,vtype=GRB.CONTINUOUS, name='x')

m.addConstrs(gp.quicksum(x[i,j] for i in proj) <= ore_disp[j] for j in collab)

m.addConstrs(gp.quicksum(x[i,j] for j in collab) == ore_req[i] for i in proj)

m.addConstr(gp.quicksum(x[i,1]*costo_ora[1] for i in proj )>=50)
m.addConstr(gp.quicksum(x[i,4]*costo_ora[4] for i in proj )>=25)

m.addConstr(gp.quicksum(x[i, 0] + x[i, 2] + x[i, 6] + x[i, 8] for i in proj) <= 70 )

m.addConstr(x[1, 3] >= 5)
m.addConstr(x[2, 7] >= 5)

m.setObjective(gp.quicksum(costo_ora[j]*x[i,j] for i in proj for j in collab), GRB.MINIMIZE)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\n Soluzione ottima trovata: \n")
    for i in proj:
        for j in collab:
            if x[i, j].X > 0.5:
                print(f"Incarico {j+1} assegnato al progetto {i+1}")
    print(f"\n Costo totale: {m.ObjVal} euro")