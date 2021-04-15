import gurobipy as gp
from gurobipy import GRB

class Graph:
    # number of subsets/locations
    m = 0

    # number of elements/targets;
    n = 0

    # edges
    edges = 0

    # cost
    c = []

    # reward
    pi = []

    # adjacency list (nodes)
    AD = []

    # budget
    alpha = 0

    # subset interdiction variable
    z = {}

    # subset selection variable
    x = {}

    # node surveillance variable
    y = {}

    MRG_Model = gp.Model('MaxRewardGain')
    RGI_Model = gp.Model('RewardGainInterdiction')

    def __init__(self, inputfile):
        '''
            Read graph from input file which must be provided at instantiation of class object.
        '''
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
        '''
            Print graph - can be used and modified for logging purposes.
        '''
        print('m = %d' % self.m)
        print('n = %d' % self.n)
        print('number of edges = %d' % self.edges)
        print('budget = %d' % self.alpha)
        for j in range(self.m):
            print('subset/location_%d' %j)
            print(self.AD[j])
            print('interdiction cost = %d' % self.c[j])

        for i in range(self.n):
            print('element/target_%d' %i)
            print('coverage reward = %d' %self.pi[i])

    def setupMRG(self):
        '''
            Set up initial MaxRewardGain (MRG) model.
        '''
        for k in range(self.m):
            self.x[k] = self.MRG_Model.addVar(vtype=GRB.BINARY, name="x_%d" %k)

        for i in range(self.n):
            self.y[i] = self.MRG_Model.addVar(vtype=GRB.BINARY, obj= -self.pi[i], name = "y_%d" %i)

        self.MRG_Model.update()

        for i in range(self.n):
            self.MRG_Model.addConstr((gp.quicksum(self.x[k] for k in self.AD[i]) >= self.y[i]), name = "coverage_%d"%i)

        self.MRG_Model.addConstr(gp.quicksum(self.x[k] for k in range(self.m)) <= self.alpha, name = "budget")
        self.MRG_Model.update()
        # self.MRG_Model.setParam
        # self.MRG_Model.optimize()

        self.MRG_Model.write('MRGModel.lp')

    def setupRGI(self):
        '''
            Set up initial RewardGainInterdiction (RGI) model.
        '''
        for k in range(self.m):
            self.z[k] = self.RGI_Model.addVar(vtype = GRB.BINARY, name = "z_%d"%k)

        self.RGI_Model.setObjective(gp.quicksum(self.z[k]*self.c[k] for k in range(self.m)), GRB.MINIMIZE)

        self.RGI_Model.update()
        # self.RGI_Model.optimize()
        self.RGI_Model.write('RGIModel.lp')

    def updateMRG(self):
        '''
            Update MRG model to reflect current interdiction policy.

            This is done by simply looping through every subset and setting an upperbound on MRG.x[k] to 0 if RGI.z[k] is equal to 1. 
            Otherwise, the upperbound for MRG.x[k] can stay at 1.
        '''
        testlist = [1 for i in range(self.m)]

        for k in range(self.m):
            if testlist[k] > 0.5:
                # set upper bound on self.x
                print(self.x[k])
                self.x[k].ub = 0
            else:
                self.x[k].lb =  1


G = Graph('dat/instance0.graph')
G.printG()
G.setupMRG()
G.setupRGI()

G.updateMRG()

