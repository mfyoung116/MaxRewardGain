import graph
from gurobipy import *

class MRG_Interdiction:
    # graph object (includes MRG_model, RGI_Model)
    G = Graph()

    # Kappa Model and vars
    KAP_Model = Model("Kappa")
    v = {}
    w = {}

    def __init__(self, graph_inputfile):
        '''
            Set up initial MRG and RGI models.
        '''
        self.G.setupMRGmodel()
        self.G.setupRGImodel()

    def get_cover(self):
        '''
            Subroutine to separate a cover using MRG, given the current interdiction policy.
        '''
        pass

    def get_kappa(self):
        '''
            Subroutine to compute RHS (kappa) for a given cover separated from MRG.
        '''
        pass

    def compress_cover(self):
        '''
            Subroutine to turn a non minimal cover into a minimal cover so the constraint can have RHS = 1.
            Not gonna write this yet, don't worry about it.
        '''
        pass

    def solve(self):
        '''
            Main algorithm to solve interdiction problem.

            Solve RGI by repeatedly solving MRG with current RGI policy (z_bar), and using KAP to find RHS for
            new constraint added to RGI (v2 - option to make covers minimal instead). Implemented with lazy cuts in gurobi.
        '''
        pass
