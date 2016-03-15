import sys
reload(sys)
sys.setdefaultencoding('utf8')

def read_file(file_name, separator = ''):
    lines = open(file_name).readlines()
    lines = [ x.strip() for x in lines ]
    if separator:
        lines = [ x.split(separator) for x in lines ]
    return lines

def features_select(features, select_list):
    print 'features_select start!'
    results = []
   # print type(features), type(features[0])
    #print select_list, features[0:3]
    for idx, feature in enumerate(features):
        print '\r', idx, 
        #print feature
        results.append( [feature[x] for x in select_list] )
    print 'features_select finish!'
    return results

