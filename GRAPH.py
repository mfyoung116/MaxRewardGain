import gurobipy as gp
from gurobipy import GRB

class Graph:

    # subsets
    l = 0 #s

    # nodes
    u = 0 #n

    # edges
    edges = 0 #m

    # cost
    c = [] #c

    # reward
    pi = [] #r

    # adjacency list (nodes)
    AD = []

    #budget
    alpha = 0 #b

    #Subset selection variable
    x = {}

    # node surveillance variable
    y = {}

    RGI_Model = gp.Model('RewardGainInterdiction')
    INTER_Model = gp.Model('Interdiction')

    #read graph
    def read(self, inputfile):
        f = open(inputfile, 'r')

        #read line 1 to assign parameter values
        line = f.readline()
        fields = str.split(line)
        self.l = int(fields[0])
        self.u = int(fields[1])
        self.edges = int(fields[2])
        self.alpha = int(fields[3])

        #read line 2 fill cost list
        line = f.readline()
        fields = str.split(line)
        for i in range(self.l):
            self.c.append(int(fields[i]))
        
        #read line 3 to fill reward list
        line = f.readline()
        fields = str.split(line)
        for j in range(self.u):
            self.pi.append(int(fields[j]))
        #read rest of lines to fill edges (adjacency)
        for j in range(self.u):
            self.AD.append([])
        for line in f:
            fields = line.split(' ')
            i = int(fields[0])
            j = int(fields[1])
            self.AD[j].append(i)

        f.close


    def printG(self):
        print('s = %d' % self.l)
        print('u = %d' % self.u)
        print('edges = %d' % self.edges)
        print('b = %d' % self.alpha)
        for j in range(self.l):
            print('subset_%d' %j)
            print(self.AD[j])
            print('cost = %d' % self.c[j])

        for i in range(self.u):
            print('node_%d' %i)
            print('reward = %d' %self.pi[i])



    def setupRGI(self, z_bar):
        #z = [1,0,1,0,0] replace "z" with "z"

        x = {}
        for k in range(self.l):
            x[k] = self.MRG_Model.addVar(vtype=GRB.BINARY, name="x_%d" %k)
        
        y = {}
        for i in range(self.u):
            y[i] = self.MRG_Model.addVar(vtype=GRB.BINARY, obj= -self.pi[i], name = "y_%d" %i)

        self.MRG_Model.update()

        for i in range(self.u):
            self.MRG_Model.addConstr((gp.quicksum(x[k] for k in self.AD[i]) >= y[i]), name = "coverage_%d"%i)

        for k in range(self.l):
            self.MRG_Model.addConstr(x[k] <= 1 - z[k], name = "interdicted_%d"%k)

        self.MRG_Model.addConstr(gp.quicksum(x[k]*self.c[k] for k in range(self.l)) <= self.alpha, name = "budget")

        self.MRG_Model.update()
        self.MRG_Model.setParam
        self.MRG_Model.optimize()

        for k in range(self.l):
            print("x_{}: {}".format(k,x[k].x))

        for i in range(self.u):
            print("y_{}: {}".format(i,y[i].x))
    
    def setupINTER(self):
        
        subs = [0,1,2,3,4]

        nodes_covered = set([])
        for k in subs:
            for i in coverage[k]:
            nodes_covered.add(i)
        
        
        
        z = {}
        for k in range(self.l):
            z[k] = self.INTER_Model.addVar(vtype = GRB.BINARY, name = "z_%d"%k)


        y = {}
        for i in range(self.u):
            y[i] = self.INTER_Model.addVar(vtype = GRB.BINARY, name = "y_%d"%i)
            
        
        
    




G = Graph()
G.read('INSTANCE0.txt')
G.setupMRG()

