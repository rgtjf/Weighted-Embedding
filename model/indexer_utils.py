import logging

log_format = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(format=log_format, datafmt='%Y-%m-%d %H:%M:%S %p',level=logging.DEBUG)

class Indexer:
	
	def __init__(self):
		self.init = False
		
	def load_index(self, file):
		logging.info('loading file: %s'%file)
		self.filename = file
		self.indexer = {}
		fp = open(file, 'r')
		for line in fp.readlines():
			fields = line.strip().split('\t')
			if self.indexer.has_key(fields[0]):
				logging.error('%s has repeat items'%file)
				exit(0)
			else:
				self.indexer[fields[0]] = (int(fields[1]), int(fields[2]))
				logging.info('index %s from %s to %s'%(fields[0], fields[1], fields[2]))
		fp.close()
		self.init = True
		return self.indexer

	# cond is a string, as the filename like 'STS...'
	def lookup(self, cond):
		if not self.init:
			print('use load_index to init first')
			exit(1)
		if not self.indexer.has_key(cond):
			logging.info('index can not find %s', cond)
			st, end = 0, -1
			indices = []
		else:
			st, end = self.indexer[cond]
			indices = range(st, end)
		return st, end
	
	def get_datasets(self):
		return self.indexer.keys()

indexer = Indexer()
indexer.load_index('input.info')

datasets = indexer.get_datasets()
datasets = zip(datasets, datasets)

label_file = 'gs.txt'
