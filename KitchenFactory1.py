# Kitchen Production Optimization Problem
#
# A company manufactures three different models of kitchens: A, B, and C.
#
# Problem Data:
# - Daily unit production costs:
#   - Model A: €1,500
#   - Model B: €2,500
#   - Model C: €2,000
#
# - Unit selling prices:
#   - Model A: €4,000
#   - Model B: €7,500
#   - Model C: €5,000
#
# - Fixed daily costs:
#   - Telephone: €150
#   - Electricity: €125
#
# Resource Constraints:
# - Available wood: 800 m²/day
# - Wood consumption per kitchen:
#   - Model A: 24 m²
#   - Model B: 27 m²
#   - Model C: 23 m²
#
# - Minimum production requirements:
#   - At least 4 units of model A
#   - At least 5 units of model B
#   - At least 6 units of model C
#
# Processing times per department (in minutes):
#            | Model A | Model B | Model C
# -----------|---------|---------|---------
# Cutting    |   10    |   30    |   25
# Painting   |   10    |   15    |   10
# Assembly   |    8    |   12    |   15
#
# Maximum daily availability per department:
# - Cutting: 20 hours (1,200 minutes)
# - Painting: 18 hours (1,080 minutes)
# - Assembly: 22 hours (1,320 minutes)
#
# Objective:
# Formulate the problem as a mathematical optimization model
# with the goal of maximizing the total daily profit.


import gurobipy as gp
from gurobipy import GRB

# Create the optimization model
m = gp.Model("KitchenFactory")

# Kitchen models
kitchen = ['A', 'B', 'C']

# Departments
departments = ['cutting', 'painting', 'assembly']

# Daily production cost per unit for each model
daily_prod_costs = {'A': 1500, 'B': 2500, 'C': 2000}

# Selling price per unit for each model
selling_prices = {'A': 4000, 'B': 7500, 'C': 5000}

# Fixed daily costs (phone + electricity)
phone_costs = 150
electricity_costs = 125
daily_costs = phone_costs + electricity_costs

# Maximum available wood per day (in square meters)
max_wood = 800

# Wood usage per unit of kitchen
wood_usage = {'A': 24, 'B': 27, 'C': 23}

# Processing time (in minutes) per model and department
times = {
    ('A', 'cutting'): 10, ('B', 'cutting'): 30, ('C', 'cutting'): 25,
    ('A', 'painting'): 10, ('B', 'painting'): 15, ('C', 'painting'): 10,
    ('A', 'assembly'): 8,  ('B', 'assembly'): 12,  ('C', 'assembly'): 15
}

# Maximum available time per department (in minutes)
max_time = {'cutting': 20 * 60, 'painting': 18 * 60, 'assembly': 22 * 60}

# Decision variables: number of kitchens to produce of each model
x = m.addVars(kitchen, name='x', vtype=GRB.INTEGER)

# Objective function: maximize total profit (revenues - production costs - fixed costs)
m.setObjective(
    sum(x[j] * (selling_prices[j] - daily_prod_costs[j]) for j in kitchen) - daily_costs,
    GRB.MAXIMIZE
)

# Minimum production constraints
m.addConstr(x['A'] >= 4, name='minA')
m.addConstr(x['B'] >= 5, name='minB')
m.addConstr(x['C'] >= 6, name='minC')

# Department time availability constraints
m.addConstrs(
    (gp.quicksum(x[r] * times[r, d] for r in kitchen) <= max_time[d] for d in departments),
    name='departmentTime'
)

# Wood usage constraint
m.addConstr(
    gp.quicksum(x[j] * wood_usage[j] for j in kitchen) <= max_wood,
    name='woodUsage'
)

# Solve the model
m.optimize()

# Output the optimal solution
if m.status == GRB.Status.OPTIMAL:
    print('Optimal production plan:')
    for r in kitchen:
        print(f"  Model {r}: {x[r].X:.0f} units")
    print(f"Maximum profit: €{m.ObjVal:.2f}")
