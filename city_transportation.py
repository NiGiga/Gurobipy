
import gurobipy as gp
from gurobipy import GRB
import numpy as np

m = gp.Model('City Transports')

costs = [3, 5, 2, 4]

capacity = [1500, 2000, 1800, 2500]

emissions = [0.5, 0.8, 0.3, 0.6]

min_qt = 4000
max_emissions = 2200

n_vars = len(costs)

x = m.addVars(n_vars, lb =0 , ub = capacity, vtype=GRB.CONTINUOUS, name = 'x')

ct1 = m.addConstr(gp.quicksum(x[i] for i in range(n_vars))>=min_qt, name='Minimo trasporto')

ct2 = m.addConstr(gp.quicksum(x[i]*emissions[i] for i in range(n_vars))<= max_emissions, name='Maximo emissione')

ct3 = m.addConstr(gp.quicksum(x[i] for i in range(n_vars))*0.6 <= x[2]+x[3], name= 'Relzione x3,x4')

ct4 = m.addConstr(x[1]>= 2*x[0], name='Relzione x1,x0')

ct5 = m.addConstr(x[2]<= (x[1]+x[3])/2, name='Relzione x3,x2,x4')

ct7 = m.addConstr(gp.quicksum(x[i] for i in range(n_vars))*0.4 <= x[0]+x[2], name= 'Relzione x3,x4')

m.setObjective(gp.quicksum(x[i]*costs[i] for i in range(n_vars)), GRB.MINIMIZE)

m.optimize()

# Output solution if optimal
if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    for i in range(n_vars):
        print(f"x[{i+1}] (Percorso {i+1}) = {x[i].X:.2f} tonnellate")
    print(f"\nCosto totale: {m.ObjVal:.2f} €")


