import gurobipy as gp
from gurobipy import GRB

class Graph:

    # number of subsets/locations
    m = 0 #s

    # number of elements/targets;
    n = 0 #n

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

    MRG_Model = gp.Model('MaxRewardGain')
    RGI_Model = gp.Model('RewardGainInterdiction')

    #read graph
    def read(self, inputfile):
        f = open(inputfile, 'r')

        #read line 1 to assign parameter values
        line = f.readline()
        fields = str.split(line)
        self.m = int(fields[0])
        self.n = int(fields[1])
        self.edges = int(fields[2])
        self.alpha = int(fields[3])

        #read line 2 fill cost list
        line = f.readline()
        fields = str.split(line)
        for i in range(self.m):
            self.c.append(int(fields[i]))
        
        #read line 3 to fill reward list
        line = f.readline()
        fields = str.split(line)
        for j in range(self.n):
            self.pi.append(int(fields[j]))
        #read rest of lines to fill edges (adjacency)
        for j in range(self.n):
            self.AD.append([])
        for line in f:
            fields = line.split(' ')
            i = int(fields[0])
            j = int(fields[1])
            self.AD[j].append(i)

        f.close


    def printG(self):
        print('s = %d' % self.m)
        print('u = %d' % self.n)
        print('edges = %d' % self.edges)
        print('b = %d' % self.alpha)
        for j in range(self.m):
            print('subset_%d' %j)
            print(self.AD[j])
            print('cost = %d' % self.c[j])

        for i in range(self.n):
            print('node_%d' %i)
            print('reward = %d' %self.pi[i])



    def setupMRG(self):
        #z = [1,0,1,0,0] replace "z" with "z"

        x = {}
        for k in range(self.m):
            x[k] = self.MRG_Model.addVar(vtype=GRB.BINARY, name="x_%d" %k)
        
        y = {}
        for i in range(self.n):
            y[i] = self.MRG_Model.addVar(vtype=GRB.BINARY, obj= -self.pi[i], name = "y_%d" %i)

        self.MRG_Model.update()

        for i in range(self.n):
            self.MRG_Model.addConstr((gp.quicksum(x[k] for k in self.AD[i]) >= y[i]), name = "coverage_%d"%i)

        #for k in range(self.m):
        #    self.MRG_Model.addConstr(x[k] <= 1 - z[k], name = "interdicted_%d"%k)

        self.MRG_Model.addConstr(gp.quicksum(x[k] for k in range(self.m)) <= self.alpha, name = "budget")

        self.MRG_Model.update()
        self.MRG_Model.setParam
        self.MRG_Model.optimize()

        #for k in range(self.m):
        #    print("x_{}: {}".format(k,x[k].x))

        #for i in range(self.n):
        #    print("y_{}: {}".format(i,y[i].x))
        
        self.MRG_Model.update()
        self.MRG_Model.write('MRGModel.lp')

    def setupRGI(self):
        
        subs = [0,1,2,3,4]

        #nodes_covered = set([])
        #for k in subs:
        #    for i in coverage[k]:
        #        nodes_covered.add(i)
        
        z = {}
        for k in range(self.m):
            z[k] = self.RGI_Model.addVar(vtype = GRB.BINARY, name = "z_%d"%k)


        y = {}
        for i in range(self.n):
            y[i] = self.RGI_Model.addVar(vtype = GRB.BINARY, name = "y_%d"%i)
    
        self.RGI_Model.setObjective(gp.quicksum(z[k]*self.c[k] for k in range(self.m)), GRB.MINIMIZE)



        self.RGI_Model.update()
        self.RGI_Model.optimize()
        self.RGI_Model.write('RGIModel.lp')
        

    def updateMRG(self, z_bar):
        pass






G = Graph()
G.read('INSTANCE0.txt')
G.setupMRG()
G.setupRGI()


