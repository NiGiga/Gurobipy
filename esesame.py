import gurobipy as gp
from gurobipy import GRB
import numpy as np

m = gp.Model('PC')

modelli = ['Basic', 'Gaming', 'Ultrabook']

stations = ['Assembly', 'Test', 'Packing']

times = {
    'Assembly': {'Basic': 1.5, 'Gaming': 3, 'Ultrabook': 2},
    'Test':     {'Basic': 1,   'Gaming': 2, 'Ultrabook': 1.5},
    'Packing':  {'Basic': 0.5, 'Gaming': 1, 'Ultrabook': 0.5},
}

limits = {'Assembly': 400, 'Test': 300, 'Packing': 150}

selling_price = {'Basic': 250, 'Gaming': 700, 'Ultrabook': 450}

x = m.addVars(modelli, lb=0, vtype=GRB.INTEGER, name='x')

for station in stations:
    m.addConstr(gp.quicksum(x[model] * times[station][model] for model in modelli) <= limits[station])

m.addConstr(x[0]>=50, name='Minimo Basic')
m.addConstr(x[1]>=30, name='Minimo Gaming')
m.addConstr(x[2]>=40, name='Minimo Ultrabook')

m.addConstr(gp.quicksum(x[i] for i in modelli)*0.5 <= x[1]+x[2])

m.addConstr(gp.quicksum(x[i] for i in modelli)<= 200)

m.addConstr(x[2]>= 0.6*x[1], name='Relzione xU,xG')



m.setObjective(gp.quicksum(x[i]*selling_price[i] for i in modelli), GRB.MAXIMIZE)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    for i in modelli:
        print(f"x[{i}] = {x[i].X:.2f} kg")
    print(f"\nCosto totale: {m.ObjVal:.2f} €")


