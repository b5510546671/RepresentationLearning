"""
Word2vec processing
"""

# The way to calling gensim is now changed as Gensim library was updated.
# E.g. model.syn0 becomes model.wv.syn0
# Please consult documentation

__author__  = "Cedric De Boom"
__status__  = "beta"
__version__ = "0.1"
__date__    = "2015 March 19th"


import numpy as np
import gensim
import cPickle
import logging
import os

# for run on server
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG, filename='/root/w2v.log', filemode='w')
# for run on windows
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG, filename='w2v.log', filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class dataIterator():
    def __init__(self, folder='.'):
        self.folder = folder
    def __iter__(self):
        for fname in os.listdir(self.folder):
            if not fname.endswith('.text'):
                continue
            for line in open(os.path.join(self.folder, fname)):
                yield line.split()


class w2v():
    def __init__(self):
        self.model = None
    def train(self, folder='.', size=400, window=5, sample=1e-4, workers=4, min_count=5, negative=10):
        data = dataIterator(folder)
        self.model = gensim.models.Word2Vec(data, size=size, window=window, sample=sample, workers=workers, min_count=min_count, negative=negative, hs=0)
    def save(self, filename):
    	logging.log(0, '...save(self, filename) was done...')
        if self.model is not None:
            logging.log(0, 'Saving w2v model...')
            self.model.init_sims(replace=True)
            self.model.save(filename)
            logging.log(0, 'Done saving w2v model')
        else:
            logging.log(1, 'No model present! Cannot save without model.')
    def save_minimal(self, filename):
    	logging.log(0, '...save_minimal(self, filename) was done...')
        if self.model is not None:
            logging.log(0, 'Saving w2v minimal model...')
            f = open(filename + '.wv.syn0.npy', 'wb')
            np.save(f, self.model.wv.syn0)
            f.close()
            f = open(filename + '.2.dump', 'wb')
            cPickle.dump(self.model.wv.vocab, f, cPickle.HIGHEST_PROTOCOL)
            f.close()
            logging.log(0, 'Done saving w2v minimal model')
        else:
            logging.log(1, 'No model present! Cannot save without model.')
    def load(self, filename=''):
        logging.log(0, 'Loading w2v model...')
        if filename.endswith('.bin'): #Word2Vec format
            self.model = gensim.models.KeyedVectors.load_word2vec_format(filename, binary=True)
        else:
            self.model = gensim.models.Word2Vec.load(filename)
        logging.log(0, 'Done loading w2v model.')
    def load_minimal(self, filename, size=400, window=5, sample=1e-4, workers=4, min_count=5, negative=10):
        logging.info('Loading w2v minimal model...')
        f = open(filename + '.wv.syn0.npy', 'rb')
        self.model = gensim.models.Word2Vec(sentences=None, size=size, window=window, sample=sample, workers=workers, min_count=min_count, negative=negative, hs=0)
        self.model.wv.syn0 = np.load(f)
        f.close()
        f = open(filename + '.2.dump', 'rb')
        self.model.wv.vocab = cPickle.load(f)
        f.close()
        logging.info('Done loading w2v minimal model.')
    def to_lower(self):
        new_vocab = {}
        for word in self.model.wv.vocab:
            lower_word = word.lower()
            if lower_word not in new_vocab:
                new_vocab[lower_word] = self.model.wv.vocab[word]
        self.model.wv.vocab = new_vocab
    def get_vector(self, word=''):
        return self.model[word]
    def exists_word(self, word=''):
        return word in self.model
    def interactive_query(self):
        while True:
            word = raw_input('Type a word: ')
            print self.get_vector(word)
    def interactive_similarity(self):
        while True:
            word1 = raw_input('Type first word: ')
            word2 = raw_input('Type second word: ')
            print self.model.similarity(word1, word2)
    def get_closest_words(self, n=10):
        while True:
            word = raw_input('Type word: ')
            print self.model.most_similar(positive=[word], negative=[], topn=n)


if __name__ == '__main__':
    w = w2v()
    # w.train(folder='../data/wiki')


    # for run on local
    w.train(folder='../data/wiki')
    w.save('/wiki_model/w2v_model_2017_09_13')
    w.save_minimal('/wiki_model/w2v_model_2017_09_13_minimal')
    
    #w.load('../data/w2v.model')
    # w.save('w2v_model_2017_09_13')
    # w.save_minimal('w2v_model_2017_09_13_minimal')
    # w.load('../data/wiki/wiki.en.text.vector')

	# for run on server
    # w.train(folder='/root/wiki_model/') # on server, use this path
    # w.save('/root/wiki_model/' + 'w2v_model_2017_09_13')  #on server, use this path
    # w.save_minimal('/root/wiki_model/' + 'w2v_model_2017_09_13_minimal') # on server, use this path



    print w.get_vector('were')