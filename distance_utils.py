import numpy as np
from scipy.stats import *

def L2_norm(vec):
	#if vec.sum() < 1e-8:
	#	return vec
	return vec/np.sqrt((vec ** 2).sum())

def f_cosine(vec1, vec2): # type: np.array, vec must be normalized
	return [(vec1 * vec2).sum()]

def f_manhattan(vec1, vec2):
	return [np.abs(vec1-vec2).sum()]

def f_euclidean(vec1, vec2):
	diff = vec1 - vec2
	return [np.sqrt((diff ** 2).sum())]

def f_stats(vec1, vec2):
	r0, p = pearsonr(vec1, vec2)
	r1, p = spearmanr(vec1, vec2)
	r2, p = kendalltau(vec1, vec2)
	return [r0, r1, r2]

def f_diff(vec1, vec2):
	return (vec1 - vec2).tolist()

fun_dict = { 
		"consine":f_cosine,
		"manhattan":f_manhattan,
		"euclidean":f_euclidean,
		"stats":f_stats,
		"diff":f_diff
		}

def all_distance(vec1, vec2, funs):
	features = []
	for fun in funs:
		val = fun_dict[fun](vec1, vec2)
		features += val
	return features
