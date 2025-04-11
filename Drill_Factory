"""
Implementation and solution using Gurobi

A company produces a drill model in two factories, A and B, with a unit selling price of 100 euros.
Production times per unit are:
- Factory A: 1.5 hours per unit
- Factory B: 2 hours per unit

Production costs are:
- Factory A: 40 euros per unit
- Factory B: 35 euros per unit

Monthly production capacities (in hours) are:
- Factory A: 420 hours
- Factory B: 330 hours

The company supplies 5 stores (X, Y, Z, W, K) with the following monthly demands:

Month 1:
- X: 150 units
- Y: 90 units
- Z: 50 units
- W: 32 units
- K: 100 units

Month 2:
- X: 30 units
- Y: 50 units
- Z: 180 units
- W: 120 units

Month 3:
- X: 0 units
- Y: 100 units
- Z: 75 units
- W: 0 units
- K: 200 units

Transportation costs (euros per unit of product):

+-----------+-----+-----+-----+-----+-----+
| Factory   |  X  |  Y  |  Z  |  W  |  K  |
+-----------+-----+-----+-----+-----+-----+
| A         | 5.0 | 4.7 | 3.8 | 3.0 | 3.9 |
| B         | 4.6 | 4.5 | 2.4 | 2.5 | 3.0 |
+-----------+-----+-----+-----+-----+-----+

Goal: Determine the optimal production plan to maximize the company's profit.
"""

import gurobipy as gp
from gurobipy import GRB
import itertools

m = gp.Model('DrillFactory')

# Selling price per unit
selling_price = 100

# Factories
factories = ['A', 'B']

# Stores
stores = ['X', 'Y', 'Z', 'W', 'K']

# Months
months = [1, 2, 3]

# Transportation costs per unit
transportation_costs = {tl_i: t_i for tl_i, t_i in zip(itertools.product(factories, stores),
                                                       [5.0, 4.7, 3.8, 3.0, 3.9, 4.6, 4.5, 2.4, 2.5, 3.0])}

# Production costs per unit for each factory
production_costs = {tl_i: t_i for tl_i, t_i in zip(itertools.product(factories, stores),
                                                   [40.0, 40.0, 40.0, 40.0, 40.0, 35.0, 35.0, 35.0, 35.0, 35.0])}

# Store demands per month
demands = {tl_i: t_i for tl_i, t_i in zip(itertools.product(months, stores),
                                          [150, 90, 50, 32, 100, 30, 50, 180, 120, 0, 100, 75, 0, 200])}

# Decision variables: number of units sent from factory f to store s in month m
x = m.addVars(months, factories, stores, name='x', vtype=GRB.CONTINUOUS)

# Monthly time capacity for each factory (in hours)
factories_time_capacity = {'A': 420, 'B': 330}

# Time needed to produce one unit for each factory
unitary_time_cost = {'A': 1.5, 'B': 2.0}

# Constraint: time used by each factory in each month must not exceed available time
m.addConstrs(
    (gp.quicksum(x[mth, f, s] * unitary_time_cost[f] for s in stores) <= factories_time_capacity[f]
     for mth in months for f in factories),
    name='factoryCapacity'
)

# Constraint: total quantity sent to each store in each month must satisfy demand
m.addConstrs(
    (gp.quicksum(x[mth, f, s] for f in factories) >= demands[mth, s]
     for mth, s in demands),
    name='storeDemand'
)

# Objective function: maximize total profit = revenue - production cost - transport cost
m.setObjective(
    gp.quicksum(x[mth, f, s] * (selling_price - production_costs[f, s] - transportation_costs[f, s])
                for mth in months for f in factories for s in stores),
    GRB.MAXIMIZE
)

m.optimize()

# Output solution if optimal
if m.status == GRB.Status.OPTIMAL:
    for mth in months:
        for f in factories:
            for s in stores:
                print(f'x[{mth},{f},{s}] = {x[mth, f, s].X:.0f}')
    print(f'Max value: {m.objVal:.2f} €')
