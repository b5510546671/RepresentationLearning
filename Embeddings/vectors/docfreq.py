"""
Calculate document frequencies for cleaned wiki corpus, based on w2v vocabulary
"""

# The way to calling gensim is now changed as Gensim library was updated.
# E.g. model.syn0 becomes model.wv.syn0
# Please consult documentation

__author__  = "Cedric De Boom"
__status__  = "beta"
__version__ = "0.1"
__date__    = "2015 April 1st"


import numpy as np
from w2v import w2v
import os

def calculate(corpus='enwiki.text', w2v_minimal_model='minimal', output_file='docfreq.npy'):
    w = w2v()
    w.load_minimal(w2v_minimal_model)
    n_words = len(w.model.wv.vocab)
    freqs = np.zeros(n_words)

    i = 0
    with open(corpus) as f:
        for line in f:
            if i % 10000 == 0:
                print "Processing line " + str(i) + "..."
            i += 1
            words = set(line.split())
            for word in words:
                if w.exists_word(word):
                    freqs[w.model.wv.vocab[word].index] += 1.0

    print 'Saving...'
    f = open(output_file, 'wb')
    np.save(f, freqs)
    f.close()
    print 'Done.'

def translate(original_w2v='original_w2v', new_w2v='new_w2v', from_docfreqs='from.npy', to_docfreqs='to.npy'):
    wn = w2v()
    wn.load_minimal(new_w2v)
    n_words = len(wn.model.wv.syn0)
    to_d = np.zeros(n_words)

    wo = w2v()
    wo.load_minimal(original_w2v)

    f = open(from_docfreqs, 'rb')
    from_d = np.load(f)
    f.close()

    #translate
    print 'Begin translation...'
    success = 0
    index = 0
    for word in wn.model.wv.vocab:
        i = wn.model.wv.vocab[word].index
        if wo.exists_word(word):
            j = wo.model.vocab[word].index
            to_d[i] = from_d[j]
            success += 1
        else:
            to_d[i] = 1.0
    print 'Success rate: ' + str(float(success)/len(wn.model.wv.vocab))

    print 'Saving...'
    f = open(to_docfreqs, 'wb')
    np.save(f, to_d)
    f.close()
    print 'Done.'


if __name__ == '__main__':
    calculate(corpus='/root/wiki_model/wiki.en.text', w2v_minimal_model='/root/wiki_model_w2v_model_2017_09_13/w2v_model_2017_09_13_minimal/w2v_model_2017_09_13_minimal', output_file='/root/wiki_model_w2v_model_2017_09_13/docfreq.dump')