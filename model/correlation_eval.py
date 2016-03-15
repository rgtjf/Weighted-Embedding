import logging
from scipy.stats import *
from utils import *
import numpy as np


def remove_unlabled(gs_tmp, sys_tmp):
	gs, sys = [], []
	if len(sys_tmp) != len(gs_tmp):
		print 'sys_tmp is not equal gs_tmp'
	for i in xrange(len(gs_tmp)):
		if not gs_tmp[i]:
			continue
		sys.append(sys_tmp[i])
		gs.append(gs_tmp[i])
	return gs, sys

def str2float(str_list):
	return [float(x) for x in str_list]

def macro(results):
	'''
	(cnt_i, value_i) in results
	'''
	cnt, result = 0, 0.0
	for x, y in results:
		result += x*y
		cnt += x
	result /= cnt
	return cnt, result

def eval(gs_list, sys_list, cands_list):
	results = []
	for (testset, trainsets) in cands_list:
		st, end = indexer.lookup(testset)
		gs_tmp = gs_all[st:end]
		sys_tmp = sys_all[st:end]
		gs, sys = remove_unlabled(gs_tmp, sys_tmp)
		gs, sys = str2float(gs), str2float(sys)
		peasonr = pearsonr(gs, sys)[0]
		results.append((len(gs), peasonr))
		logging.info("(%s,%s)\t%.4f\t%d\n" % (x, y, peasonr, len(gs)))   
	cnt, result = macro(results)
	logging.info("(%s,%s)\t%.4f\t%d\n" % ('all', 'all', result, cnt)) 

