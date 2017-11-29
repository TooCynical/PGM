import numpy as np
import copy

from pgmpy.models import FactorGraph
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference import VariableElimination


# Return a uniform factor on the given variable.
def uniform_factor(var):
    return DiscreteFactor([var], [2], np.array([[1.0, 1.0]]))

# Compute marginal distribution for given variable.
def brute_force(marginal, factors, variables):
    # First multiply all factors
    res = factors[0].copy()
    for fac in factors[1:]:
        res.product(fac)

    # Then marginalize each variable besides the jth.
    for var in variables:
        if var != marginal:
            res.marginalize([var])

    return res.values / sum(res.values)

def create_double_edge(up, down, factor):
    e1 = Edge(up, down, factor, 'UP')
    e2 = Edge(down, up, factor, 'DOWN')
    
    up.add_edge(e1)
    up.add_edge(e2)
    
    down.add_edge(e1)
    down.add_edge(e2)
    
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
            
            
    # Sends all messages in the given direction (up or down).        
    def send_messages(self, direction):
        for e in self.out_edges:
            if e.di == direction:
                e.message = self.message(e)
            

    # Compute message along given edge.        
    def message(self, e):
        message = uniform_factor(e.head.var)
        marginals = [self.var]

        # Compute product of all messages/factors not send by recipient.
        for f in self.in_edges:
            if f.tail.var != e.head.var:
                message.product(f.message)

        # Multiply message by edge-factor.
        message.product(e.factor)
                    
        # Marginalize over sender variable.
        message.marginalize([self.var])

        return message

    # TODO: Add normalization.
    def marginal(self):
        ret = uniform_factor(self.var)
        for e in self.in_edges:
            ret.product(e.message)
        ret = ret.values / sum(ret.values)
        return ret
        

# Edge class that contains a head/tail node, a factor and a message (from tail to head).              
class Edge:
    def __init__(self, head, tail, factor, di):
        self.head = head
        self.tail = tail
        self.factor = factor
        self.di = di
        
        self.message = uniform_factor(head.var)
        




if __name__ == "__main__":
    # Create variablenodes, 0th entry is dummy s.t. X[1] = 'X1' etc.
    X = [VarNode("X" + str(i)) for i in range(15)]

    # Set all factors
    f12 =   DiscreteFactor(['X1', 'X2'], [2, 2], np.array([[0.7, 0.3, 0.1, 0.5]]))
    f13 =   DiscreteFactor(['X1', 'X3'], [2, 2], np.array([[0.7, 0.1, 0.2, 0.2]]))
    f14 =   DiscreteFactor(['X1', 'X4'], [2, 2], np.array([[0.3, 0.3, 0.3, 0.3]]))
    f25 =   DiscreteFactor(['X2', 'X5'], [2, 2], np.array([[0.8, 0.4, 0.5, 0.8]]))
    f26 =   DiscreteFactor(['X2', 'X6'], [2, 2], np.array([[0.9, 0.5, 0.5, 1.0]]))
    f37 =   DiscreteFactor(['X3', 'X7'], [2, 2], np.array([[0.1, 0.3, 0.1, 0.5]]))
    f38 =   DiscreteFactor(['X3', 'X8'], [2, 2], np.array([[0.1, 0.4, 0.1, 0.1]]))
    f39 =   DiscreteFactor(['X3', 'X9'], [2, 2], np.array([[0.2, 0.7, 0.1, 0.7]]))
    f410 =  DiscreteFactor(['X4', 'X10'], [2, 2], np.array([[0.3, 0.8, 0.5, 0.5]]))
    f511 =  DiscreteFactor(['X5', 'X11'], [2, 2], np.array([[0.1, 0.8, 0.6, 0.5]]))
    f712 =  DiscreteFactor(['X7', 'X12'], [2, 2], np.array([[0.4, 0.9, 0.9, 0.9]]))
    f1013 = DiscreteFactor(['X10', 'X13'], [2, 2], np.array([[0.5, 0.1, 0.5, 0.9]]))
    f1014 = DiscreteFactor(['X10', 'X14'], [2, 2], np.array([[0.5, 0.2, 0.1, 0.3]]))
    factors = [f12, f13, f14, f26, f37, f38, f39, f410, f511, f712, f1013, f1014]

    # Create edges
    create_double_edge(X[5], X[11], f511)
    create_double_edge(X[2], X[5], f25)
    create_double_edge(X[2], X[6], f26)
    create_double_edge(X[7], X[12], f712)
    create_double_edge(X[3], X[7], f37)
    create_double_edge(X[3], X[8], f38)
    create_double_edge(X[3], X[9], f39)
    create_double_edge(X[10], X[13], f1013)
    create_double_edge(X[10], X[14], f1014)
    create_double_edge(X[4], X[10], f410)
    create_double_edge(X[1], X[2], f12)
    create_double_edge(X[1], X[3], f13)
    create_double_edge(X[1], X[4], f14)

    reverse_order = range(1, 15)
    order = range(1, 15)
    order.reverse()

    # Send messages upwards.
    for i in order:
        X[i].send_messages("UP")

    # Send messages downwards.
    for i in reverse_order:
        X[i].send_messages("DOWN")

    # Print all marginals.
    for i in reverse_order:
        print "X" + str(i) + ":\t", X[i].marginal()
        # print "X" + str(i) + ":\t", brute_force("X" + str(i), factors, ["X" + str(x) for x in range(1, 15)])
    
