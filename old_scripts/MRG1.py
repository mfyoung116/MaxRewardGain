import gurobipy as gp
from gurobipy import GRB

#### Sets and Sub-Sets of a small instance

#U={a,b,c,d,e,f,g,h,i}
#S={S1,S2,S3,S4,S5}

#S1={a,b,c}
#S2={a,b,h,i}
#S3={b,c,d,e,f,h}
#S4={d,e,g}
#S5={e,f,g,h,i}

#### Reward from each node
#1(a)=13
#2(b)=7
#3(c)=15
#4(d)=11
#5(e)=12
#6(f)=14
#7(g)=9
#8(h)=17
#9(i)=13

# Cost to "pick" each Sub-Set
#1(S1)=32
#2(S2)=38
#3(S3)=63
#4(S4)=30
#5(S5)=49

budget = 120
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

subsets, coverage, cost = gp.multidict({
    0 : [{0,1,2}, 32],
    1 : [{1,2,7,8}, 38],
    2 : [{1,2,3,4,5,7}, 63],
    3 : [{3,4,6}, 30],
    4 : [{4,5,6,7,8}, 49]
})

z = [1,0,1,0,0]

#Model Building
m = gp.Model("Max_Reward_Gain_1")

#Variable generation
x = {}
for k in subsets:
    x[k] = m.addVar(vtype=GRB.BINARY, name="x_%d" %k)

y = {}
for i in nodes:
    y[i] = m.addVar(vtype=GRB.BINARY, obj= -reward[i], name = "y_%d" %i)

m.update()

#Constraints

for i in nodes:
    m.addConstr((gp.quicksum(x[k] for k in covered_by[i]) >= y[i]), name = "coverage_%d"%i)

for k in subsets:
    m.addConstr(x[k] <= 1 - z[k], name = "interdicted_%d"%k)

m.addConstr(gp.quicksum(x[k]*cost[k] for k in subsets) <= budget, name = "budget")

m.update()

m.setParam

m.optimize()

for k in subsets:
    print("x_{}: {}".format(k,x[k].x))

for i in nodes:
    print("y_{}: {}".format(i,y[i].x))
#add a comment
