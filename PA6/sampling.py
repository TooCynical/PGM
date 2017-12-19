# Lucas Slot,   lfh.slot@gmail.com  (2984451).
#
# University of Bonn
# November 2017
#
# Tables.py

import pyAgrum as grum

# Initialize net on four binary variables
net = grum.BayesNet("FactorGraph")
for var in "ABCDEFGH":
	net.add(var, 2)

# Add dependency arcs
net.addArc('A', 'C')
net.addArc('B', 'D')
net.addArc('C', 'D')
net.addArc('C', 'H')
net.addArc('C', 'D')

# Set CPTs.
net.cpt('R').fillWith([0.8, 0.2])
net.cpt('S').fillWith([0.9, 0.1])

net.cpt('J')[{'R': 0}] = [0.8, 0.2]
net.cpt('J')[{'R': 1}] = [0.,  1.]

net.cpt('T')[{'R': 0, 'S': 0}] = [1.,  0.]
net.cpt('T')[{'R': 0, 'S': 1}] = [0.1, 0.9]
net.cpt('T')[{'R': 1, 'S': 0}] = [0.,  1.]
net.cpt('T')[{'R': 1, 'S': 1}] = [0.,  1.]


# For ease of reading.
prob = net.cpt
B = [0, 1]
BB = [(0,0), (1,0), (0,1), (1,1)]
BBB = [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]


def forward_sample(t):
    # Sample R
    r = (1 if random.random() > prop('R')[r] else 0)

    
    
    
    
