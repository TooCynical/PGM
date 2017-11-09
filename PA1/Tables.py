# Lucas Slot,   lfh.slot@gmail.com  (2984451).
#
# University of Bonn
# November 2017
#
# Tables.py

import pyAgrum as grum

# Initialize net on four binary variables
net = grum.BayesNet("Sprinkler")
for var in "TJRS":
	net.add(var, 2)

# Add dependency arcs
net.addArc('R', 'J')
net.addArc('S', 'T')
net.addArc('R', 'T')

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

def p_TS(t, s):
	return sum([prob('T')[{'R': r, 'S': s}][t] * \
		        prob('S')[s] * \
		        prob('R')[r] \
		        for r in B])


def p_S_given_T(s, t):
	numerator   = sum([prob('T')[{'R' : r, 'S' : s}][t] * \
					   prob('R')[r] * \
					   prob('S')[s] \
					   for r in [0, 1]])
	
	denominator = sum([prob('T')[{'R' : r, 'S' : s}][t] * 
					   prob('R')[r] * \
					   prob('S')[s] \
					   for r, s in BB])

	return numerator / denominator


def p_S_given_TJ(s, t, j):
	numerator = sum([prob('J')[{'R': r}][j] * \
                     prob('T')[{'R': r, 'S': s}][t] * \
                     prob('R')[r] * \
                     prob('S')[s] \
					 for r in B])

	denominator = sum([prob('J')[{'R': r}][j] * \
					  prob('T')[{'R': r, 'S': s}][t] * \
					  prob('R')[r] * \
                      prob('S')[s] \
					  for r, s in BB])
	
	return numerator / denominator

print "P(T, S):"
for i, j in BB:
	print i, j, "||", p_TS(i, j)
print 

print "P(S | T):"
for i, j in BB:
	print i, j, "||", p_S_given_T(i, j)
print

print "P(S | T,J):"
for i, j, k in BBB:
	print i, j, k, "||", p_S_given_TJ(i, j, k)
print
