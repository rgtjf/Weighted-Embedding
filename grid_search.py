
candidate = [ i/10.0 for i in range(6, 16, 2)]

print candidate


#n, v, a, r, #
param_grid = [
 	{ 'n': candidate, 'v': candidate, 'a': candidate, 'r': candidate, '#': candidate }
 	#{'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
 ]


def eval(param_dict):
	#print param_dict
	#print cnt
	global cnt 
	cnt = cnt + 1
	pass
	
	VecDict
	ConfigDict
	Input 
	Gs
	Eval_func()


def search(param_dict, candidata_dict):
	if not candidata_dict:
		eval(param_dict)
	else:
		key, value_list = candidata_dict.items()[0]
		newcandidata_dict = candidata_dict.copy()
		newcandidata_dict.pop(key)
		for value in value_list:
			param_dict[key] = value
			search(param_dict, newcandidata_dict)
	# 

cnt = 0
search({}, param_grid[0])
print cnt