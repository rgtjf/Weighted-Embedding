import numpy as np
import cPickle
from collections import defaultdict
import sys, re, string
import nltk
import math
from nltk.corpus import stopwords
from scipy.stats import *
reload(sys)
sys.setdefaultencoding('utf-8') 

stopwords = stopwords.words('english')
puncts = string.punctuation + '\r\n``\'\''


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

## remove punctuations nums and stopwords	
def tokenize(text, config):
	removal = config['input.remove']
	if config['input.lower']:
		text = text.lower()
	tokens = nltk.word_tokenize(text)
	for key in removal:
		if key == "stopwords":
			tokens = [ token for token in tokens if token not in stopwords ]
		elif key == "punctuations":
			tokens = [ token for token in tokens if token not in puncts ]
		else:
			print "Key error [input.remove]: %s"%key
			sys.exit(0)
	return tokens

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
	for line in fp.readlines():
		fields = line.strip().split(delimiter)
		s1 = fields[indices[0]]
		s2 = fields[indices[1]]
		t1 = tokenize(s1, config)
		t2 = tokenize(s2, config)
		for word in set(t1):
			vocab[word] += 1
		for word in set(t2):
			vocab[word] += 1
		'''
		label = fields[indices[2]]
		datum = { "label": label,
				  "text": (t1, t2),
				  "num_words": (len(t1), len(t2))
				  }
		'''
		datum = { "text": (t1, t2),
				  "num_words": (len(t1), len(t2))
				  }
		max_l = max2(max2(len(t1), len(t2)), max_l)
		revs.append(datum)
	fp.close()
	return revs, vocab, max_l
	
def load_google_vec(fname, vocab):
	"""
	Loads 300x1 word vecs from Google (Mikolov) word2vec
	"""
	word_vecs = {}
	with open(fname, "rb") as f:
		header = f.readline()
		vocab_size,layer1_size = map(int, header.split())
		binary_len = np.dtype('float32').itemsize * layer1_size
		for line in xrange(vocab_size):
			word = []
			while True:
				ch = f.read(1)
				if ch == ' ':
					word = ''.join(word)
					break
				if ch != '\n':
					word.append(ch)   
			if word in vocab:
			   word_vecs[word] = np.fromstring(f.read(binary_len), dtype='float32')  
			else:
				f.read(binary_len)
	return word_vecs

def load_plain_vec(fname, vocab):
	"""
	Loads word vecs from word vector files
	"""
	word_vecs = {}
	fp = open(fname, 'r')
	for line in fp.readlines():
		fs = line.strip().split(' ')
		word = fs[0]
		if word in vocab:
			vec = []
			for val in fs[1:]:
				vec.append(float(val))
			word_vecs[word] = np.asarray(vec)
	fp.close()
	return word_vecs

def add_unknown_words(word_vecs, vocab, min_df=1, k=300):
	"""
	For words that occur in at least min_df documents, create a separate word vector.	
	0.25 is chosen so the unknown vectors have (approximately) same variance as pre-trained ones
	"""
	for word in vocab:
		if word not in word_vecs and vocab[word] >= min_df:
			word_vecs[word] = np.random.uniform(-0.25,0.25,k)  

'''
def calc_idf(revs):
	words = []
	for i in xrange(len(revs)):
		rev = revs[i]
		toks = set(rev["text"][0] + rev["text"][1])
		words += list(toks)
	vdist = nltk.FreqDist(words)
	doc_num = len(revs)
	idf_dict = {}
	for key in vdist:
		idf_dict[key] = math.log(float(doc_num)/float(vdist[key]))/math.log(2)
	return idf_dict
'''


fun_dict = { 
		"consine":f_cosine,
		"manhattan":f_manhattan,
		"euclidean":f_euclidean,
		"stats":f_stats,
		"diff":f_diff
		}

def build_sent(words, w2v_dict, dim, convey, weight):
	"""
	Transforms sentence into a list of indices. Pad with zeroes.
	"""
	vdist = nltk.FreqDist(words)
	length = float(len(words))
	vec = np.zeros((dim,))
	for word in vdist:
		if convey == 'simple' or convey == 'idf':
			w = weight[word]
		elif convey == 'tfidf':
			w = (vdist[word]/length) * weight[word]
		else:
			print 'Unknown convey: %s' % convey
			sys.exit(0)
		w2v = vdist[word] * w * w2v_dict[word]
		vec = vec + w2v
	return vec

def build_features_helper(sent1, sent2, funs):
	features = []
	for fun in funs:
		val = fun_dict[fun](sent1, sent2)
		features += val
	return features

def build_features(revs, w2v_dict, config):
	conveys = config['word2vec.convey']
	dim = config['word2vec.dim']
	funs = config['feature.funs']
	weight = {}
	for key in w2v_dict:
		weight[key] = 1
	if 'idf' in conveys or 'tfidf' in conveys:
		weight = calc_idf(revs)
		assert len(weight) == len(w2v_dict), 'length error'
	features = defaultdict(list)
	#Ys = {}
	for convey in conveys:
		for i in xrange(len(revs)):
			rev = revs[i]
			sent1 = build_sent(rev["text"][0], w2v_dict, dim, convey, weight)
			sent2 = build_sent(rev["text"][1], w2v_dict, dim, convey, weight)
			#print rev["text"][0], sent1
			#print rev["text"][1], sent2
			feats = build_features_helper(L2_norm(sent1), L2_norm(sent2), funs)
			features[i] += feats
			#Ys[i] = rev["label"]
			print '\r%d'%i,
			sys.stdout.flush()
	#dat = []
	#for i in xrange(len(revs)):
	#	dat.append((Ys[i], features[i]))
	return features

# model each sentence as a vector
if __name__=="__main__":
	if len(sys.argv) < 2:
		print "Usage: run config file"
		sys.exit(0)
	config = read_config(sys.argv[1])
	print config
	print "loading data...",		
	revs, vocab, max_l = read_data(config)
	print "data loaded!"
	print "number of sentence pairs: " + str(len(revs))
	print "vocab size: " + str(len(vocab))
	print "max sentence length: " + str(max_l)
	print "loading word2vec vectors...",
	wfile = config['word2vec.file']
	formatt = config['word2vec.format'] 
	if formatt == 'bin':
		w2v = load_google_vec(wfile, vocab)
	elif formatt == 'plain':
		w2v = load_plain_vec(wfile, vocab)
	else:
		print "Unknown format: %s"%formatt
		sys.exit(0)
	print "word2vec loaded!"
	print "num words already in word2vec: " + str(len(w2v))
	add_unknown_words(w2v, vocab, k=config['word2vec.dim'])
	print "word_matrix size:(%d,%d)" % (len(w2v), config['word2vec.dim'])
	
	features = build_features(revs, w2v, config)
	#assert len(features) == len(Ys), 'Length error'
	print '\nfeature number: %d'%(len(features[0]))
	fw1 = open(config['output.feature.file'], 'w')
	#fw2 = open(config['output.label.file'], 'w')
	for i in xrange(len(revs)):
		feats = features[i]
		fw1.write('%s\n'%(' '.join([str(0.0) if math.isnan(val) else str(val) for val in feats])))
		#fw2.write(Ys[i] + '\n')
	fw1.close()
	#fw2.close()

	print "dataset created!"
	
def posTransform(pos):
	if pos == 'NN' or pos == 'NNS' or pos == 'NNP' or pos == 'NNPS':
		pos = 'n'
	elif pos =='VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos=="VBP" or pos=="VBZ":
		pos = 'v'
	elif pos == 'JJ' or pos == 'JJR' or pos == 'JJS':
		pos = 'a'
	elif pos == 'RB' or pos == 'RBR' or pos == 'RBS':
		pos = 'r'
	else:
		pos = '#'
	return pos
