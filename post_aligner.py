import sys
import json
from nltk.corpus import stopwords
from scipy.stats import *
reload(sys)
sys.setdefaultencoding('utf8')

stopwords = stopwords.words('english')
punctuations = ['(',')',',','-','_',':','{','}','[','/',']' ]

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

def frange(x, y, jump):
	res = []
	while x <= y:
		res.append(x)
		x += jump
	return res

gl_weight = [frange(0.3, 0.5, 0.1), frange(0.7,0.9,0.1),frange(1.3,1.51,0.1),frange(1.3,1.51,0.1),frange(1.1,1.31,0.1),frange(0.7,0.9,0.1)]
print gl_weight
gl_w = [0.5, 0.8, 1.5, 1.5, 1.2, 0.7]
def get_weight(word):
	pos_tag = posTransform(word[2])
	ner_tag = word[3]
	weight = 0.0
	if ner_tag != 'O':
		weight += gl_w[0]
	if pos_tag == 'v':
		weight += gl_w[1]
	elif pos_tag == 'n':
		weight += gl_w[2]
	elif pos_tag == 'a':
		weight += gl_w[3]
	elif pos_tag == 'r':
		weight += gl_w[4]
	else:
		weight += gl_w[5]
	return weight
	
def load_origin_pairs(input_file):
	fp = open(input_file)
	sents = []
	for line in fp:
		line = line.strip().split('\t')
		sents.append((line[0], line[1]))
	return sents
		

def load_from_sent(sent):
	sent = json.loads(sent)
	#sent = [ x[0] for x in sent ]
	return sent

def load_align(annotated_file = 'output0.txt'):
	align = []
	annotate = open(annotated_file).readlines()
	for idx, line in enumerate(annotate):
		sent = json.loads(line.strip())
		align.append(sent)
	return align

def load_sent_pairs(input_file = 'input.parse.txt'):
	sent_pairs = open(input_file).readlines()
	for idx, sent_pair in enumerate(sent_pairs):
		sent_pair = sent_pair.strip().split('\t')
		sent1 = sent_pair[0]
		sent2 = sent_pair[1]
		sent1 = load_from_sent(sent1)
		sent2 = load_from_sent(sent2)
		sent_pairs[idx] = (sent1, sent2)
	return sent_pairs

origin_sents = load_origin_pairs('one_input.txt')
sent_pairs = load_sent_pairs('one_input.parse.txt')
align = load_align('one_output0.txt')

def calc_sim(input_file, annotated_file):
	scores = []
	for ids, sent_pair in enumerate(sent_pairs):
		sent_align = align[ids]
		sent1 = sent_pair[0]
		sent2 = sent_pair[1]
		#sent1 = origin_sents[ids][0].split()
		#sent2 = origin_sents[ids][1].split()
		#align aligned, stopwords
		sent1_aligned = [ 0 for x in xrange(len(sent1)+1) ]
		sent2_aligned = [ 0 for x in xrange(len(sent2)+1) ]
	
		
#		for idx, word in enumerate(sent1):
#			if word in stopwords:
#				sent1_aligned[ idx + 1 ] = 2
#			if word in punctuations:
#				sent1_aligned[ idx + 1 ] = 2
#		for idx, word in enumerate(sent2):
#			if word in stopwords:
#				sent2_aligned[ idx + 1 ] = 2
#			if word in punctuations:
#				sent2_aligned[ idx + 1 ] = 2
	
		for word in sent_align:
			sent1_aligned[ word[0] ] = 1
			sent2_aligned[ word[1] ] = 1
	#		print sent1[word[0]-1],
	#		print sent2[word[1]-1],
	
		#calc all and aligned except stopwords
		sent1_sum, sent2_sum, sent1_ali, sent2_ali = 0, 0, 0, 0
		for idx, word in enumerate(sent1):
			weight = get_weight(word)
			if sent1_aligned[idx+1] == 1:
				sent1_ali += weight
				sent1_sum += weight
			elif sent1_aligned[idx+1] == 0:
				sent1_sum += weight
		for idx, word in enumerate(sent2):
			weight = get_weight(word)
			if sent2_aligned[idx+1] == 1:
				sent2_ali += weight
				sent2_sum += weight
			elif sent2_aligned[idx+1] == 0:
				sent2_sum += weight
	
		#score = (1.0*sent1_ali/sent1_sum + 1.0*sent2_ali/sent2_sum) #score = 1.0*(len(words1)+len(words2))/(sent1_sum+sent2_sum)
		score = 1.0 * (sent1_ali + sent2_ali) / (len(origin_sents[ids][0].split()) + len(origin_sents[ids][1].split()))
	#	score = 1.0 * (sent1_ali + sent2_ali) / (sent1_sum + sent2_sum)
	#	print sent1_sum, sent2_sum
#		print len(words1), len(words2), len(origin_sents[ids][0].split()), len(origin_sents[ids][1].split())
		scores.append(score)
#		if ids == 10:
#			break
	return scores

def eval_all(gs_all, sys_all):
	gs, sys = [], []
	for idx in xrange(len(gs_all)):
		if not gs_all[idx]:
			continue
		gs.append(float(gs_all[idx]))
		sys.append(float(sys_all[idx]))
	peasonr = pearsonr(gs, sys)[0]
	return peasonr

scores = calc_sim('one_input.parse.txt', 'output0.txt')
fw = open('feature.align.stop', 'w')
scores = map(str, scores)
print >>fw, '\n'.join(scores)
fw.close()
'''
fw = open('one_post', 'w')
gs_all = open('one_gs.txt').readlines()
gs_all = [ x.strip() for x in gs_all ]
bestscore = 0.0
best = []
idx = 0
for x0 in gl_weight[0]:
	for x1 in gl_weight[1]:
		for x2 in gl_weight[2]:
			for x3 in gl_weight[3]:
				for x4 in gl_weight[4]:
					for x5 in gl_weight[5]:
						gl_w = [x0, x1, x2, x3, x4, x5]
						#print gl_w
						print '\r',idx,
						idx = idx + 1
						sys_all = calc_sim('one_input.parse.txt', 'output0.txt')
						score = eval_all(gs_all, sys_all)
						print >>fw, score, gl_w 
						if score > bestscore:
							bestscore = score
							best = gl_w
							print 'best', bestscore, best
'''

