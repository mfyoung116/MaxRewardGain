import GRAPH
from gurobipy import *

class MRG_Interdiction:
    # graph object (includes MRG_model, RGI_Model)
    G = Graph()

    # Kappa Model
    KAP_Model = Model("Kappa")

    def __init__(self, graph_inputfile):
        '''
            Basically just set up the graph fully, and the initial models for
            BLK_Model, KAP_Model
        '''
        self.G.read(graph_inputfile)
        self.G.setupMRGmodel()
        self.G.setupRGImodel()


    def solve(self):
        '''
            Main algorithm to solve interdiction problem
        '''
        
