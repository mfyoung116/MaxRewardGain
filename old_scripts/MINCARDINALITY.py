import gurobipy as gp
from gurobipy import GRB

budget = 1000
nodes,reward, covered_by = gp.multidict({
    0: [13, {0}], 
    1: [7, {0,1,2}], 
    2: [15, {0,1,2}], 
    3: [11, {2,3}],
    4: [12, {2,3,4}], 
    5: [14, {2,4}], 
    6: [9, {3,4}], 
    7: [17, {1,2,4}], 
    8: [13, {1,4}]
})

beta = 67
subsets, coverage, cost = gp.multidict({
    0 : [{0,1,2}, 32],
    1 : [{1,2,7,8}, 38],
    2 : [{1,2,3,4,5,7}, 63],
    3 : [{3,4,6}, 30],
    4 : [{4,5,6,7,8}, 49]
})

z = [0,0,1,0,0]

m = gp.Model("MinCard")

#variable generation

x = {}
for k in subsets:
    x[k] = m.addVar(vtype=GRB.BINARY, name="x_%d" %k)

y = {}
for i in nodes:
    y[i] = m.addVar(vtype=GRB.BINARY, name = "y_%d" %i)

m.update()

#Constraints

m.addConstr(gp.quicksum(y[i]*reward[i] for i in y) >= beta)

for i in nodes:
    m.addConstr((gp.quicksum(x[k] for k in covered_by[i]) >= y[i]), name = "coverage_%d"%i)

for k in subsets:
    m.addConstr(x[k] <= 1 - z[k], name = "interdicted_%d"%k)

m.addConstr(gp.quicksum(x[k]*cost[k] for k in subsets) <= budget, name = "budget")

m.update()

m.setObjective(gp.quicksum(x[k] for k in subsets), GRB.MINIMIZE)

m.optimize()


for k in subsets:
    print("x_{}: {}".format(k,x[k].x))

for i in nodes:
    print("y_{}: {}".format(i,y[i].x))