import gurobipy as gp
from gurobipy import GRB

m = gp.Model('Trasloco')

c_j = [10,20,15,10,16,9,17,13,18,14,14,16,13,18,14,16,19,13,11,17]
t_j = [6,8,3,12,8,5,3,10,5,2,14,16,13,18,14,16,19,13,11,17]
cf_i = [80,170,50]
work = list(range(20))
trasp = list(range(3))

x = m.addVars(trasp,work, vtype=GRB.BINARY, name="x")

for i in trasp:
    m.addConstr(gp.quicksum(x[i,j]*c_j[j] for j in work) <= cf_i[i])

for j in work:
    m.addConstr(gp.quicksum(x[i,j] for i in trasp) == 1)

diff = m.addVars(trasp[:-1], work, vtype=GRB.CONTINUOUS, name="diff")

for i in trasp[:-1]:
    for j in work:
        exp = (x[i,j]-x[i+1,j])*t_j[j]
        m.addConstr(diff[i,j] >= exp)
        m.addConstr(diff[i,j] >= -exp)


m.setObjective(gp.quicksum(diff[i, j] for i in trasp[:-1] for j in work), GRB.MINIMIZE)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    for i in trasp:
        for j in work:
            if x[i, j].X > 0.5:
                print(f"Attività {j+1} assegnata al trasportatore {i+1}")
    print(f"\nValore obiettivo: {m.ObjVal}")
