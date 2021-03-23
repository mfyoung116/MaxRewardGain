import gurobipy as gp
from gurobipy import GRB

class Graph:

    # subsets
    s = 0

    # nodes
    n = 0

    # edges
    m = 0

    # cost
    c = []

    # reward
    r = []

    # adjacency list (nodes)
    AD = []

    #budget
    b = 0
    #follower model
    MRG_model = gp.Model("MaxRewardGain")

    #Subset selection variable
    x = {}

    # node surveillance variable
    y = {}

    #read graph
    def read(self, inputfile):
        f = open(inputfile, 'r')

        #read line 1 to assign parameter values
        line = f.readline()
        fields = str.split(line)
        self.s = int(fields[0])
        self.n = int(fields[1])
        self.m = int(fields[2])
        self.b = int(fields[3])

        #read line 2 fill cost list
        line = f.readline()
        fields = str.split(line)
        for i in range(self.s):
            self.c.append(int(fields[i]))
        
        #read line 3 to fill reward list
        line = f.readline()
        fields = str.split(line)
        for j in range(self.n):
            self.r.append(int(fields[j]))
        #read rest of lines to fill edges (adjacency)
        for j in range(self.n):
            self.AD.append([])
        for line in f:
            fields = line.split(' ')
            i = int(fields[0])
            j = int(fields [1])
            self.AD[j].append(i)

        f.close


    def printG(self):
        print('s = %d' % self.s)
        print('n = %d' % self.n)
        print('m = %d' % self.m)
        print('b = %d' % self.b)
        for j in range(self.s):
            print('subset_%d' %j)
            print(self.AD[j])
            print('cost = %d' % self.c[j])

        for i in range(self.n):
            print('node_%d' %i)
            print('reward = %d' %self.r[i])



G = Graph()
G.read('INSTANCE0.txt')



