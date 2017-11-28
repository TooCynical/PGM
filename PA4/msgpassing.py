import numpy as np
import copy

from pgmpy.models import FactorGraph
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference import VariableElimination


def uniform_factor(var):
    return DiscreteFactor([var], [2], np.array([[0.5, 0.5]]))


def create_double_edge(up, down, factor):
    e1 = Edge(up, down, factor, 'UP')
    e2 = Edge(down, up, factor, 'DOWN')
    
    up.add_edge(e1)
    up.add_edge(e2)
    
    down.add_edge(e1)
    down.add_edge(e2)
    
    
class OrderedTree:
    def __init__(self, nodes):
        self.nodes = nodes;

        
class VarNode:
    def __init__(self, var):
        self.var = var

        self.out_edges = []
        self.in_edges = []

    def add_edge(self, e):
        if e.head.var == self.var:
            self.in_edges.append(e)
        elif e.tail.var == self.var:
            self.out_edges.append(e)
        else:
            raise ValueError("Invalid edge added!")
            
            
    def send_upward_message(self):
        for e in self.out_edges:
            if e.dir == 'UP':
                e.message = self.message(e.head)
            
    def message(self, other):
        message = uniform_factor(other.var)
        
        # Compute product of all messages/factors not send by recipient.
        for e in self.in_edges:
            message.product(e.factor)
            message.product(e.message)            
                
        # Marginalize over all variables except the recipient.
        for var in message.scope:
            if var != other.var:
                message.marginalize([var])
        
        return message
        
                
class Edge:
    def __init__(self, head, tail, factor, di):
        self.head = head
        self.tail = tail
        self.factor = factor
        self.di = di
        
        self.message = uniform_factor(head.var)
        

f12 = DiscreteFactor(['X1', 'X2'], [2, 2], np.array([[4.75, 4.95, 0.05, 0.25]]))
X1 = VarNode("X1")
X2 = VarNode("X2")
create_double_edge(X1, X2, f12)

