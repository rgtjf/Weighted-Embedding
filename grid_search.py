
candidate = [ i/10.0 for i in range(6, 16, 2)]

#n, v, a, r, #
param_grids = [
 	{ 'n': candidate, 'v': candidate, 'a': candidate, 'r': candidate, '#': candidate }
 	#{'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
 ]

def product(param_grid):
	'''
	test = {'n': [1,2], 'a': [2, 3]}
	it = product(test)
	try:
		while True:
			x = it.next()
			print x
	except StopIteration:
		pass
	'''
	pools = param_grid.values()
	result = [[]]
	for pool in pools:
		result = [x+[y] for x in result for y in pool]
	for prod in result:
		yield dict(zip(param_grid.keys(), prod))
