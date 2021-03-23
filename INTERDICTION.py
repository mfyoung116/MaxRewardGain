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

beta = 70
subsets, coverage, cost = gp.multidict({
    0 : [{0,1,2}, 32],
    1 : [{1,2,7,8}, 38],
    2 : [{1,2,3,4,5,7}, 63],
    3 : [{3,4,6}, 30],
    4 : [{4,5,6,7,8}, 49]
})

m = gp.Model("Interdictor")

s = [0,1,2,3,4]

nodes_covered = set([])
for k in s:
    for i in coverage[k]:
        nodes_covered.add(i)


#Variable Generation

z = {}
for k in s:
    z[k] = m.addVar(vtype = GRB.BINARY, name = "z_%d"%k)


y = {}
for i in nodes_covered:
    y[i] = m.addVar(vtype = GRB.BINARY, name = "y_%d"%i)

m.update()


#Constraints Generation

for k in s:
    for i in coverage[k]:
        m.addConstr(y[i] >= 1 - z[k], name = "interdicted_%d,%d"%(k,i))

m.addConstr(gp.quicksum(y[i]*reward[i] for i in nodes_covered) <= beta, name = "min_reward")


m.setObjective(gp.quicksum(z[k] for k in s), GRB.MINIMIZE)

m.update()

m.optimize()

for k in s:
    if z[k].x > 0.5:
        print('%s = %d'%(z[k].varName, z[k].x))

for i in nodes_covered:
    if y[i].x > 0.5:
        print('%s = %d'%(y[i].varName, y[i].x))
