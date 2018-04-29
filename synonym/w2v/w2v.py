import gensim
from gensim.models.keyedvectors import KeyedVectors
from synonym.config import config

_configer = config["development"]
BASEDIR = _configer.data_basedir
W2V_FILE = BASEDIR+"/synonym/word2vec/words.vector"

class W2vSim():
    
    def __init__(self):
        self.word_vectors = KeyedVectors.load_word2vec_format(W2V_FILE,binary=True)
    
    def sim(self,w1,w2):
        try:
            sim_value = self.word_vectors.similarity(w1,w2)
            return sim_value
        except KeyError as e:
            return -1

if __name__ == '__main__':
    wv = W2V()
    print(wv.sim("轿车","汽车"))