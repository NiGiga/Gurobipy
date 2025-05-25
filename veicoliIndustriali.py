"""
Una industria automobilistica utilizza cinque differenti linee di montaggio (A, B, C, D ed E) per l'assemblaggio di
veicoli industriali e veicoli agricoli. Il settore marketing ha previsto una forte richiesta dei due tipi di veicoli
per il mese successivo, per cui è possibile vende-re un qualsiasi quantitativo che l'industria è in grado di assemblare.
Nello stabilire il piano di produzione per il mese successivo gli elementi da considerare sono:
a) dalla vendita dei veicoli l'industria è in grado di realizzare un profitto unitario pari a 6.000 € per i veicoli
industriali e a 2.000 € per i veicoli agricoli;
b) nel mese successivo, per l'assemblaggio dei due tipi di veicoli, la linea A potrà es-
sere impegnata per un totale di 180 ore complessive, la linea B per 135 ore mentre
la linea C per 200 ore. Inoltre, le ore di utilizzo complessivo delle linee A e D non
potranno superare le 300 ore mentre le linee C ed E complessivamente dovranno
essere usate per almeno 100.
c) ciascun veicolo industriale per l’assemblaggio richiede le seguenti ore sulle varie li-
nee (20, 10, 5, 15, 20) mentre per un veicolo agricolo le ore richieste sono (12, 15,
10, 7, 9);
d) l'industria utilizza un ulteriore impianto per il controllo di qualità, specificatamente
per i veicoli industriali e agricoli assemblati. A seguito di accordi sindacali l'impian-
to deve rimanere attivo per un numero di ore pari almeno al 25% della capacità a
regime, calcolata in 100 ore mensili, ma senza limiti superiori.
e) sono richieste 20 ore per testare un veicolo industriale e 10 ore per un veicolo agri-
colo;
f) il settore “gestione del personale” ha individuato che, per garantire una distribuzio-
ne ottimale del personale lungo le linee di montaggio, il numero di veicoli agricoli
assemblati deve essere pari almeno alla metà del numero di veicoli industriali as-
semblati;
g) il responsabile della distribuzione ha segnalato che la più grande concessionaria di zona ha richiesto per il mese
successivo almeno 4 veicoli, senza specificare il nu -
mero per ogni tipo. Inoltre, un’altra concessionaria ha gia’ richiesto 3 veicoli indu-
striali e 2 veicoli agricoli.
Sulla base di tali considerazioni, il problema è pianificare la produzione di veicoli indu-striali e agricoli per il
mese successivo, ovvero, stabilire il mix ottimale di prodotti con l'obiettivo di massimizzare il profitto. Si formuli
e su risolva tale problema.
"""

import gurobipy as gp
from gurobipy import GRB

linee = ['A', 'B', 'C', 'D', 'E', 'T']
veicoli = ['industriali', 'agricoli']
profitto ={
    'industriali': 6000,
    'agricoli': 2000
}
ore_necessarie = {
    ('industriali', 'A'): 20, ('industriali', 'B'): 10, ('industriali', 'C'): 5, ('industriali', 'D'): 15, ('industriali', 'E'): 20, ('industriali', 'T'): 20,
    ('agricoli', 'A'): 12, ('agricoli', 'B'): 15, ('agricoli', 'C'): 10, ('agricoli', 'D'): 7, ('agricoli', 'E'): 9, ('agricoli', 'T'): 10
}


m = gp.Model('Veicoli')

x = m.addVars(linee, veicoli, lb=0, vtype=GRB.INTEGER, name='x')

m.setObjective(gp.quicksum(profitto[j]*x['T', j] for j in veicoli), GRB.MAXIMIZE)

m.addConstrs(x[i,'industriali'] == x[j,'industriali'] for i in linee for j in linee if i != j)

m.addConstrs(x[i,'agricoli'] == x[j,'agricoli'] for i in linee for j in linee if i != j)

m.addConstr(gp.quicksum(ore_necessarie[(j, 'A')]*x['A', j] for j in veicoli) <= 180)

m.addConstr(gp.quicksum(ore_necessarie[(j, 'B')]*x['B', j] for j in veicoli) <= 135)

m.addConstr(gp.quicksum(ore_necessarie[(j, 'C')]*x['C', j] for j in veicoli) <= 200)

m.addConstr(gp.quicksum((ore_necessarie[(j, 'A')]*x['A', j])+(ore_necessarie[(j, 'D')]*x['D', j]) for j in veicoli) <= 300)

m.addConstr(gp.quicksum((ore_necessarie[(j, 'C')]*x['C', j])+(ore_necessarie[(j, 'C')]*x['C', j]) for j in veicoli) >= 100)

m.addConstr(gp.quicksum(x['T', j]*ore_necessarie[(j, 'T')] for j in veicoli) >=25)

m.addConstr(gp.quicksum(x[i, 'agricoli'] for i in linee) >= 0.5*gp.quicksum(x[i, 'industriali'] for i in linee))

m.addConstr(gp.quicksum(x['T', j]  for j in veicoli)>= 4)

m.addConstrs(x['T', j] >= (2 if j == 'agricoli' else 3) for j in veicoli)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print("\nSoluzione ottima trovata:\n")
    for i in linee:
        for j in veicoli:
            print(f"x[{i},{j}] = {x[i, j].X} veicoli")
    print(f"\nGuadagno totale: {m.ObjVal:.2f} $")



