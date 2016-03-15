from nlp_utils import *
from collections import defaultdict
import json

def read_config(config_file):
    fp = open(config_file)
    config = {}
    for line in fp.readlines():
        line = line.strip()
        if len(line)== 0 or line[0] == '#':
            continue
        fields = line.split('=')
        config[fields[0].strip()] = fields[1].strip()
    fp.close()
    ## change type
    if config['input.delimiter'] == '\\t':
        config['input.delimiter'] = '\t'
    config['word2vec.dim'] = int(config['word2vec.dim'])
    indices = [ int(val) for val in config['indices'].split(',') ]
    config['indices'] = indices
    config['feature.funs'] = config['feature.funs'].split(',')
    config['input.remove'] = config['input.remove'].split(',')
    config['word2vec.convey'] = config['word2vec.convey'].split(',')
    config['input.lower'] = config['input.lower'] == 'True'
    return config


def max2(a, b):
    return a if a > b else b

def read_data(config):
    """
    Loads data .
    """
    filepath = config['input.file']
    delimiter = config['input.delimiter']
    indices = config['indices']
    cnt = 0
    max_l = 0
    revs = []
    vocab = defaultdict(float)
    fp = open(filepath, 'r')
    lines = fp.readlines()
    fw = open('tmp.txt', 'w')
    for idx, line in enumerate(lines):
        fields = line.strip().split(delimiter)
        s1 = fields[indices[0]]
        s2 = fields[indices[1]]
        t1, p1 = nlp.tokenize(s1, config['input.lower'], *config['input.remove'])
        t2, p2 = nlp.tokenize(s2, config['input.lower'], *config['input.remove'])
       
        json.dump(zip(t1, p1), fw)
        print >>fw, '\t',
        json.dump(zip(t2, p2), fw)
        print >>fw

        for word in set(t1):
            vocab[word] += 1
        for word in set(t2):
            vocab[word] += 1
        datum = { "text": (t1, t2),
                  "pos": (p1, p2),
                  "num_words": (len(t1), len(t2))
                  }
        max_l = max2(max2(len(t1), len(t2)), max_l)
        revs.append(datum)
    fp.close()
    return revs, vocab, max_l
    

def read_data_from_tmp(config):
    '''
    Loads data from tmp.txt.
    '''
    filepath = config['input.file']
    delimiter = config['input.delimiter']
    indices = config['indices']
    cnt = 0
    max_l = 0
    revs = []
    vocab = defaultdict(float)
    fp = open('tmp.txt', 'r')
    lines = fp.readlines()
    for idx, line in enumerate(lines):
        #fields = line.strip().split(delimiter)
        #s1 = fields[indices[0]]
        #s2 = fields[indices[1]]
        sent_pair = line.strip().split('\t')
        s1 = json.loads(sent_pair[0])
        s2 = json.loads(sent_pair[1])
        t1, p1 = zip(*s1)
        #t1 = list(t1)
        #p1 = list(p1)
        t2, p2 = zip(*s2)
        #t2 = list(t2)
        #p2 = list(p2)
        #t1, p1 = nlp.tokenize(s1, config['input.lower'], *config['input.remove'])
        #t2, p2 = nlp.tokenize(s2, config['input.lower'], *config['input.remove'])
        for word in set(t1):
            vocab[word] += 1
        for word in set(t2):
            vocab[word] += 1
        datum = { "text": (t1, t2),
                  "pos": (p1, p2),
                  "num_words": (len(t1), len(t2))
                  }
        max_l = max2(max2(len(t1), len(t2)), max_l)
        revs.append(datum)
    fp.close()
    return revs, vocab, max_l
    
