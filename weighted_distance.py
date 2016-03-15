from config_utils import *
from distance_utils import *
from nlp_utils import *
from embedding_utils import *
from utils import *
from grid_search import *
import sys,math


it = product(param_grids[0])
it.next()
pos_dict = it.next()
print pos_dict

def pos_weight(pos):
    pos_t = POS_transform(pos)
    w_pos = pos_dict[pos_t]
    return w_pos
    pass

def build_sent(words, poss, w2v_dict, dim, convey, weight):
    '''
    Transforms sentence into a list of indices. Pad with zeroes.
    '''
    poss = dict(zip(words, poss))
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
        w_pos = pos_weight(poss[word])
        w2v = vdist[word] * w * w2v_dict[word] * w_pos
        vec = vec + w2v
    return vec


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
            sent1 = build_sent(rev["text"][0], rev["pos"][0], w2v_dict, dim, convey, weight)
            sent2 = build_sent(rev["text"][1], rev["pos"][1], w2v_dict, dim, convey, weight)
            #print rev["text"][0], sent1
            #print rev["text"][1], sent2
            feats = all_distance(L2_norm(sent1), L2_norm(sent2), funs)
            features[i] += feats
            #Ys[i] = rev["label"]
            print '\r%d'%i,
            sys.stdout.flush()
    #dat = []
    #for i in xrange(len(revs)):
    #    dat.append((Ys[i], features[i]))
    return features


# model each sentence as a vector
if __name__=="__main__":
    if len(sys.argv) < 2:
        print "Usage: run config file"
        sys.exit(0)
    config = read_config(sys.argv[1])
    print config
    print "loading data...",        
    #revs, vocab, max_l = read_data(config)
    revs, vocab, max_l = read_data_from_tmp(config)
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
    
