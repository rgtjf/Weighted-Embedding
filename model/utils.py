import sys
reload(sys)
sys.setdefaultencoding('utf8')

def read_file(file_name, separator = ''):
	lines = open(file_name).readlines()
	lines = [ x.strip() for x in lines ]
	if seperator:
		lines = [ x.split(seperator) for x in lines ]
	return lines

def features_select(features, select_list):
	print 'features_select start!'
	results = []
	for idx, feature in enumerate(features):
		print '\r', idx, 
		results.append( [feature[x] for x in select_list] )	
	return results


