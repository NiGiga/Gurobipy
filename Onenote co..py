"""
 La Onenote Co. produce un singolo prodotto per quattro clienti in tre differenti stabilimenti. I tre stabilimenti produrranno
rispettivamente 60, 80 e 40 unità nel prossimo periodo. La ditta si impegnata a vendere 40 unità al cliente 1,
60 unità al cliente 2 e almeno 20 unità al cliente 3. Entrambi i clienti 3 e 4 inoltre desiderano
avere la possibilità di poter comprare le unità restanti. Il profitto netto associato alla spedizione dell'unità
dallo stabilimento i per la vendita al cliente} è dato dalla seguente tabella:
                                Cliente
                        1       2       3       4
                    1   800    700     500    200
Stabilimento        2   500    200     100    300
                    3   600    400     300    500

Il management desidera conoscere quante unità vendere ai clienti 3 e 4 e quante unità spedire da ciascuno degli
stabilimenti a ciascuno dei clienti con l'obiettivo di massimizzare il profitto.
(a) Formulare questo problema come problema di trasporto in
    cui la funzione obiettivo deve essere massimizzata e si costruisca l'opportuna tabella dei parametri contenenti
    i profitti unitari.

(b) Formulare questo problema di trasporto con l' usuale obiettivo di minimizzazione il costo complessivo convertendo
    la tabella dei parametri del punto (a) in una che contiene i costi unitari anziché i profitti unitari.

"""

import gurobipy as gp
from gurobipy import GRB

clienti = list(range(4))
stabilimenti = list(range(3))

produzione = [60, 80, 40]

profitto = [[800, 700, 500, 200],
            [500, 200, 100, 300],
            [600, 400, 300, 500]]

m = gp.Model('OnenoteCo')

x = m.addVars(clienti, stabilimenti, lb=0, vtype=GRB.INTEGER, name='x')

# m.setObjective(gp.quicksum(profitto[j][i]*x[i,j] for j in stabilimenti for i in clienti ), GRB.MAXIMIZE) #(a)
m.setObjective(gp.quicksum(profitto[j][i]*x[i,j] for j in stabilimenti for i in clienti ), GRB.MINIMIZE) #(b)


m.addConstrs(gp.quicksum(x[i,j] for i in clienti)<=produzione[j] for j in stabilimenti)

m.addConstr(gp.quicksum(x[0,j] for j in stabilimenti)== 40)

m.addConstr(gp.quicksum(x[1,j] for j in stabilimenti)== 60)

m.addConstr(gp.quicksum(x[2,j] for j in stabilimenti)>= 20)

m.addConstr(gp.quicksum(x[i, j] for j in stabilimenti for i in clienti) == 180)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\n Soluzione ottima trovata: \n")
    for i in clienti:
        for j in stabilimenti:
            if x[i, j].X > 0.5:
                print(f"Vendita al cliente {i+1} allo stabilimento {j+1}")
    # print(f"\n Profitto totale: {m.ObjVal} euro") #(a)
    print(f"\n Costo totale: {m.ObjVal} euro") #(b)