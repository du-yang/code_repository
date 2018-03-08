import codecs
import numpy as np
import nltk
import pycrfsuite
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import jieba
import jieba.posseg as pseg

import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')



""" not use this data
# Read data file and parse the XML
with codecs.open("/data/carlzzhang/test/NER/python-crfsuite_test/n3-collection/reuters.xml", "r", "utf-8") as infile:
    soup = bs(infile, "html5lib")

docs = []
for elem in soup.find_all("document"):
    texts = []

    # Loop through each child of the element under "textwithnamedentities"
    for c in elem.find("textwithnamedentities").children:
        if type(c) == Tag:
            if c.name == "namedentityintext":
                label = "N"  # part of a named entity
            else:
                label = "I"  # irrelevant word
            for w in c.text.split(" "):
                if len(w) > 0:
                    texts.append((w, label))
    docs.append(texts)

for texts in docs:
    print "\n".join(["-".join([w, label]) for w, label in texts])
    print

data = []
for i, doc in enumerate(docs):

    # Obtain the list of tokens in the document
    tokens = [t for t, label in doc]

    # Perform POS tagging
    tagged = nltk.pos_tag(tokens)

    # Take the word, POS tag, and its label
    data.append([(w, pos, label) for (w, label), (word, pos) in zip(doc, tagged)])
"""

def word2features(doc, i):
    word = doc[i][0]
    postag = doc[i][1]

    # Common features for all words
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag
    ]

    # Features for words that are not
    # at the beginning of a document
    if i > 0:
        word1 = doc[i-1][0]
        postag1 = doc[i-1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:word.isdigit=%s' % word1.isdigit(),
            '-1:postag=' + postag1
        ])
    else:
        # Indicate that it is the 'beginning of a document'
        features.append('BOS')

    # Features for words that are not 
    # at the end of a document
    if i < len(doc)-1:
        word1 = doc[i+1][0]
        postag1 = doc[i+1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:word.isdigit=%s' % word1.isdigit(),
            '+1:postag=' + postag1
        ])
    else:
        # Indicate that it is the 'end of a document'
        features.append('EOS')

    return features

# A function for extracting features in documents
def extract_features(doc):
    return [word2features(doc, i) for i in range(len(doc))]

# A function fo generating the list of labels for each document
def get_labels(doc):
    return [label for (token, postag, label) in doc]

def get_data(filename):
    data = {}
    for line in open(filename, "r"):
        line = line.strip()
        sen = line
        segs = pseg.cut(sen)

        char_segs = []
        for seg in segs:
            for char in seg.word:
                char_segs.append([char, seg.flag])

        #data.append([(c, s, "NONE") for c, (c, s) in zip(sen, char_segs)])

        data[sen] = [(c, s, "NONE") for c, (c, s) in zip(sen, char_segs)]

        """
        for c, (c, s) in zip(sen, char_segs):
            print(" ".join([c, s, ""]).encode("utf8"))
        print
        """

    X = [extract_features(doc) for doc in data.values()]
    y = [get_labels(doc) for doc in data.values()]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    for features, labels in zip(X, y):
        for feature, label in zip(features, labels):
            print(" ".join(feature) + " " + " ".join(label))
        print()

    return X_train, X_test, y_train, y_test

def get_data_with_pos():
    data = []
    doc = []
    for line in open("/data/carlzzhang/test/Chinese-Literature-NER-RE-Dataset/ner/all.txt.pos", "r"):
        line = line.strip()
        if len(line) == 0:
            data.append(doc)
            doc = []
        else:
            array = line.split(" ")
            w, pos, label = array
            doc.append((w, pos, label))

    print(len(data))

    X = [extract_features(doc) for doc in data]
    y = [get_labels(doc) for doc in data]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    for features, labels in zip(X, y):
        for feature, label in zip(features, labels):
            print(" ".join(feature) + " " + " ".join(label))
        print()

    return X_train, X_test, y_train, y_test

def train(X_train, X_test, y_train, y_test):
    trainer = pycrfsuite.Trainer(verbose=True)

    # Submit training data to the trainer
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)

    # Set the parameters of the model
    trainer.set_params({
        # coefficient for L1 penalty
        'c1': 0.1,

        # coefficient for L2 penalty
        'c2': 0.01,  

        # maximum number of iterations
        'max_iterations': 200,

        # whether to include transitions that
        # are possible, but not observed
        'feature.possible_transitions': True
    })

    # Provide a file name as a parameter to the train function, such that
    # the model will be saved to the file when training is finished
    trainer.train('crf.model')

def predict(X_train, X_test, y_train, y_test):
    # Generate predictions
    tagger = pycrfsuite.Tagger()
    tagger.open('crf.model')
    y_pred = [tagger.tag(xseq) for xseq in X_test]

    """
    # Let's take a look at a random sample in the testing set
    i = 12
    for x, y in zip([x[1].split("=")[1] for x in X_test[i]], y_pred[i]):
        print("%s (%s)" % (x, y))
    """

    labels = {}
    for i in range(len(y_pred)):
        for y in y_pred[i]:
            if y not in labels:
                labels[y] = len(labels)

    for k, v in labels.items():
        print(" ".join([k, str(v)]))

    predictions = np.array([tag for row in y_pred for tag in row])
    truths = np.array([tag for row in y_test for tag in row])
    #print(classification_report(truths, predictions, target_names=labels.keys()))
    print(classification_report(truths, predictions))

    #for xseq in zip(X_test, y_pred):

    """
    # Create a mapping of labels to indices
    labels = {"N": 1, "I": 0}

    # Convert the sequences of tags into a 1-dimensional array
    predictions = np.array([labels[tag] for row in y_pred for tag in row])
    truths = np.array([labels[tag] for row in y_test for tag in row])

    # Print out the classification report
    print(classification_report(truths, predictions, target_names=["I", "N"]))
    """

    """
    # classification_report
    from sklearn.metrics import classification_report
    y_true = [0, 1, 2, 2, 2]
    y_pred = [0, 0, 2, 2, 1]
    target_names = ['class 0', 'class 1', 'class 2']
    print(classification_report(y_true, y_pred, target_names=target_names))
    #
    """

def predict_batch(filename):
    # Generate predictions
    tagger = pycrfsuite.Tagger()
    tagger.open('crf.model')

    for line in open(filename, "r"):
        line = line.strip()
        sen = line # utf8
        segs = pseg.cut(sen)

        r = [[char, seg.flag] for seg in segs for char in seg.word]#; print len(r)
        f = extract_features(r)
        t = tagger.tag(f)#; print len(tags)
        for (c, s), t_ in zip(r, t):
            print "\t".join([c, t_])
        print

if __name__ == "__main__":
    """
    X_train, X_test, y_train, y_test = get_data_with_pos()
    #train(X_train, X_test, y_train, y_test)
    #predict(X_train, X_test, y_train, y_test)
    """

    """
    filename = "/data/carlzzhang/test/Chinese-Literature-NER-RE-Dataset/ner/all.txt.sen"
    X_train, X_test, y_train, y_test = get_data(filename)
    predict(X_train, X_test, y_train, y_test)
    """

    filename = "/data/carlzzhang/test/Chinese-Literature-NER-RE-Dataset/ner/all.txt.sen"
    predict_batch(filename)

