import GRAPH
from gurobipy import *

class MRG_Interdiction:
    # graph object (includes MRG_model)
    G = Graph()

    # Interdiction Model (BLK for block)
    BLK_Model = Model("Interdiction")

    # Kappa Model
    KAP_Model = Model("Kappa")

    def __init__(self, graph_inputfile):
        '''
            Basically just set up the graph fully, and the initial models for
            BLK_Model, KAP_Model
        '''
        G.read(graph_inputfile)
        # G.setupMRGmodel() // doesn't exist yet in my version so will need fixing


    def solve(self):
        '''
            Main algorithm to solve interdiction problem
        '''
        
