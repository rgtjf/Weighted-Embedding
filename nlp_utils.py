<<<<<<< HEAD
import nltk, string
from nltk.corpus import stopwords
import json, requests
import sys,math

#=============================================================================
#
#`1 NLTK
#	a)stopwords, punctation
#	b)tokenize(text)
#	c)POS_transform(POS)
#
#=============================================================================

stopwords = stopwords.words('english')

puncts = string.punctuation + '\r\n``\'\''

## remove punctuations nums and stopwords	
def tokenize(text, lower=True, *removal):
	#removal = config['input.remove']
	#if config['input.lower']:
	if lower:
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


def POS_transform(pos):
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


#=============================================================================
#
#`2 StanfordCoreNLP
#	nlp.parse(text)
#	output json
#
#=============================================================================



class StanfordCoreNLP:

    def __init__(self, server_url):
        if server_url[-1] == '/':
            server_url = server_url[:-1]
        self.server_url = server_url

    def annotate(self, text, properties=None):
        if not properties:
            properties = {}
        r = requests.get(
            self.server_url, params={
                'properties': str(properties)
            }, data=text)
        output = r.text
        if ('outputFormat' in properties 
             and properties['outputFormat'] == 'json'):
            try:
				output = json.loads(output, strict=False)
            except:
                pass
        return output

    def tokensregex(self, text, pattern, filter):
        return self.regex('/tokensregex', text, pattern, filter)

    def semgrex(self, text, pattern, filter):
        return self.regex('/semgrex', text, pattern, filter)

    def regex(self, endpoint, text, pattern, filter):
        r = requests.get(
            self.server_url + endpoint, params={
                'pattern':  pattern,
                'filter': filter
            }, data=text)
        output = r.text
        try:
            output = json.loads(r.text)
        except:
            pass
        return output

class StanfordNLP:
	def __init__(self):
		self.server = StanfordCoreNLP('http://localhost:9000')

	def parse(self, text):
		output = self.server.annotate(text, properties={
			'annotators': 'tokenize,lemma,ssplit,pos,depparse,parse,ner',
			'outputFormat': 'json'
		})
		return output

nlp = StanfordNLP()
=======
import nltk, string
from nltk.corpus import stopwords
import json, requests
import sys,math

#=============================================================================
#
#`1 NLTK
#	a)stopwords, punctation
#	b)tokenize(text)
#	c)POS_transform(POS)
#
#=============================================================================

stopwords = stopwords.words('english')

puncts = string.punctuation + '\r\n``\'\''

## remove punctuations nums and stopwords	
def tokenize(text, lower=True, *removal):
	#removal = config['input.remove']
	#if config['input.lower']:
	if lower:
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


def POS_transform(pos):
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


#=============================================================================
#
#`2 StanfordCoreNLP
#	nlp.parse(text)
#	output json
#
#=============================================================================



class StanfordCoreNLP:

    def __init__(self, server_url):
        if server_url[-1] == '/':
            server_url = server_url[:-1]
        self.server_url = server_url

    def annotate(self, text, properties=None):
        if not properties:
            properties = {}
        r = requests.get(
            self.server_url, params={
                'properties': str(properties)
            }, data=text)
        output = r.text
        if ('outputFormat' in properties 
             and properties['outputFormat'] == 'json'):
            try:
				output = json.loads(output, strict=False)
            except:
                pass
        return output

    def tokensregex(self, text, pattern, filter):
        return self.regex('/tokensregex', text, pattern, filter)

    def semgrex(self, text, pattern, filter):
        return self.regex('/semgrex', text, pattern, filter)

    def regex(self, endpoint, text, pattern, filter):
        r = requests.get(
            self.server_url + endpoint, params={
                'pattern':  pattern,
                'filter': filter
            }, data=text)
        output = r.text
        try:
            output = json.loads(r.text)
        except:
            pass
        return output

class StanfordNLP:
	def __init__(self):
		self.server = StanfordCoreNLP('http://localhost:9000')

	def parse(self, text):
		output = self.server.annotate(text, properties={
			'annotators': 'tokenize,lemma,ssplit,pos,depparse,parse,ner',
			'outputFormat': 'json'
		})
		return output

nlp = StanfordNLP()
>>>>>>> bob/master
