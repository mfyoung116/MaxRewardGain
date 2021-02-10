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

budget = 140
nodes,reward = gp.multidict({
    0: 13, 1: 7, 2: 15, 3: 11,
    4: 12, 5: 14, 6: 9, 7: 17, 
    8:13
})

subsets, coverage, cost = gp.multidict({
    0 : [{1,2,3}, 32],
    1 : [{2,3,8,9}, 38],
    2 : [{2,3,4,5,6,8}, 63],
    3 : [{4,5,7}, 30],
    4 : [{5,6,7,8,9}, 49]
})

#Model Building
m = gp.Model("Max_Reward_Gain_1")

#Variable generation
pick = m.addVars(len(subsets), vtype=GRB.BINARY, name="pick")
is_covered = m.addVars(len(nodes), vtype=GRB.BINARY, name="is_covered")

#Constraint
m.addConstrs((gp.quicksum(pick[i] for i in subsets if j in coverage[i]) >= is_covered[j]
                        for j in nodes), name="Pick_cover")

m.addConstr(pick.prod(cost) <= budget, name = "budget")

m.setObjective(is_covered.prod(reward), GRB.MAXIMIZE)

m.optimize()