import numpy as np

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
