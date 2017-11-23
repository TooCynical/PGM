import numpy as np
import copy

from pgmpy.models import FactorGraph
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference import VariableElimination


# Create variables (as strings).
v = ["X" + str(i) for i in range(1,9)]


# Create Factors.
f1 = DiscreteFactor(['X1'], [2], np.array([[4.95, 0.05]]))
f2 = DiscreteFactor(['X2'], [2], np.array([[2.5, 2.5]]))

f31 = DiscreteFactor(['X3', 'X1'], [2, 2], np.array([[4.75, 4.95, 0.05, 0.25]]))
f52 = DiscreteFactor(['X5', 'X2'], [2, 2], np.array([[3.5, 2.0, 1.5, 3.]]))
f42 = DiscreteFactor(['X4', 'X2'], [2, 2], np.array([[4.95, 4.5, 0.05, 0.5]]))
f68 = DiscreteFactor(['X6', 'X8'], [2, 2], np.array([[4.75, 0.1, 0.25, 4.9]]))

f843 = DiscreteFactor(['X8', 'X4', 'X3'], [2, 2, 2], np.array([[5., 0., 0., 0., 0., 5., 5., 5.]]))
f758 = DiscreteFactor(['X7', 'X5', 'X8'], [2, 2, 2], np.array([[4.5, 1.5, 1., 0.5, 0.5, 3.5, 4., 4.5]]))

f = [f1, f2, f31, f52, f42, f68, f843, f758]


def create_model():
	# Init graph.
	G = FactorGraph()

	# Add variable nodes to model.
	G.add_nodes_from(v)

	# Add factor nodes to model.
	G.add_nodes_from(f)

	# Add edges to the model.
	edges = [('X1', f1), ('X2', f2),    \
	         ('X3', f31), ('X1', f31),  \
	         ('X5', f52), ('X2', f52),  \
	         ('X4', f42), ('X2', f42),  \
	         ('X6', f68), ('X8', f68),
	         ('X8', f843), ('X4', f843), ('X3', f843),
	         ('X7', f758), ('X5', f758), ('X8', f758)]
	G.add_edges_from(edges)
	
	# Finally add all factors.
	G.add_factors(f1, f2, f31, f52, f42, f68, f843, f758)

	assert(G.check_model())
	return G


# Compute marginal distribution for given variable.
def brute_force(marginal, factors=f, variables=v):
	# First multiply all factors
	res = factors[0].copy()
	for fac in factors[1:]:
		res.product(fac)

	# Then marginalize each variable besides the jth.
	for var in variables:
		if var != marginal:
			res.marginalize([var])

	return res.values / sum(res.values)


# Eliminate one variable from a factor list and return the result.
def eliminate(var, factors):
	in_scope = []
	remaining = []

	# Separate factors between those that do and do not have var in their scope.
	for fac in factors:
		if var in fac.scope():
			in_scope.append(fac)
		else: 
			remaining.append(fac)
	
	# Find the product of all factors with var in their scope.
	if in_scope:
		prod = in_scope[0].copy()
		for fac in in_scope[1:]:
			prod.product(fac)
		# Then marginalize var from this product.
		prod.marginalize([var])
		# And add it to the returned factors.
		remaining.append(prod)
	return remaining


# Compute marginal for given factors (ordered)
def sum_product(marginal, factors=f, variables=v):
	current_factors = copy.copy(factors)
	for var in variables:
		if var != marginal:
			current_factors = eliminate(var, current_factors)
	
	# Multiply all remaining factors
	res = current_factors[0].copy()
	for fac in current_factors[1:]:
		res.product(fac)
	return res.values / sum(res.values)




order = ['X5', 'X2', 'X4', 'X3', 'X6', 'X1', 'X8', 'X7']
for marginal in v:
	print 'Marganalizing:', marginal
	print 'Brute force: \t', brute_force(marginal)
	print 'Sum-product: \t', sum_product(marginal)

# G = create_model()
# Z = G.get_partition_function()
# inference = VariableElimination(G)
# verify = inference.query(['X2'], elimination_order=['X1', 'X3', 'X4', 'X5', 'X6', 'X8', 'X7'])['X2']
# print 'Verification: \t', verify.values / sum(verify.values)


