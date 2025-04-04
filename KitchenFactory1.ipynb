#%% md
# Problema di Ottimizzazione della Produzione di Cucine

Un’azienda produce tre modelli differenti di cucine: **A**, **B** e **C**.

## **Dati del problema**

- **Costi unitari giornalieri di produzione**
  - Modello A: **1.500 €**
  - Modello B: **2.500 €**
  - Modello C: **2.000 €**

- **Prezzi unitari di vendita**
  - Modello A: **4.000 €**
  - Modello B: **7.500 €**
  - Modello C: **5.000 €**

- **Costi fissi giornalieri**
  - Spese telefoniche: **150 €**
  - Consumo di energia elettrica: **125 €**

## **Vincoli sulle risorse**

- **Disponibilità del legno**: **800 m²/giorno**
- **Consumo di legno per cucina**
  - Modello A: **24 m²**
  - Modello B: **27 m²**
  - Modello C: **23 m²**

- **Produzione minima richiesta**
  - Almeno **4** cucine di tipo A
  - Almeno **5** cucine di tipo B
  - Almeno **6** cucine di tipo C

## **Tempi di lavorazione nei reparti**

| Reparto       | Modello A | Modello B | Modello C |
|--------------|----------|----------|----------|
| **Taglio**       | 10 min    | 30 min    | 25 min    |
| **Verniciatura** | 10 min    | 15 min    | 10 min    |
| **Montaggio**    | 8 min     | 12 min    | 15 min    |

- **Disponibilità massima giornaliera per reparto**
  - Taglio: **20 ore** (**1.200 min**)
  - Verniciatura: **18 ore** (**1.080 min**)
  - Montaggio: **22 ore** (**1.320 min**)

## **Obiettivo del problema**

Formulare il problema come un **modello di ottimizzazione matematica** con l'obiettivo di **massimizzare il profitto giornaliero complessivo**.

#%%
import gurobipy as gp
from gurobipy import GRB

m = gp.Model("KitchenFactory")

kitchen = ['A', 'B', 'C']
departments = ['taglio', 'verniciatura', 'montaggio']

daily_prod_costs = {'A': 1500, 'B': 2500, 'C': 2000}

selling_prices = {'A': 4000, 'B': 7500, 'C': 5000}


phone_costs = 150
electricity_costs = 125
daily_costs = phone_costs+electricity_costs

max_wood = 800

wood_usage = {'A': 24, 'B': 27, 'C': 23}



times = {('A', 'taglio'): 10, ('B', 'taglio'): 30, ('C', 'taglio'): 25,
         ('A', 'verniciatura'): 10, ('B', 'verniciatura'): 15, ('C', 'verniciatura'): 10,
         ('A', 'montaggio'): 8, ('B', 'montaggio'): 12, ('C', 'montaggio'): 15}

max_tme = {'taglio': 20 * 60, 'verniciatura': 18 * 60, 'montaggio': 22 * 60}

x = m.addVars(kitchen, name='x', vtype=GRB.INTEGER)


m.setObjective((sum(x[j] * (selling_prices[j] - daily_prod_costs[j]) for j in kitchen) - daily_costs), GRB.MAXIMIZE)

m.addConstr(x['A'] >= 4)
m.addConstr(x['B'] >= 5)
m.addConstr(x['C'] >= 6)

m.addConstrs((gp.quicksum(x[r] * times[r, m] for r in kitchen) <= max_tme[m] for m in departments), name='workTime')

m.addConstr(gp.quicksum(x[j] * wood_usage[j] for j in kitchen ) <= max_wood, name='woodUsage')

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print('Optimal solution:')
    for r in kitchen:
        print(f"{r}: {x[r].X:.0f}")
    print(f"Profit: {m.ObjVal:.2f}")
