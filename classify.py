from __future__ import division

from postdata import posts

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC

def has_title(p):
    return "title" in p
posts = {k: post for k,post in posts.iteritems() if has_title(post)}

CUTOFF = 1
HOLDOUT = .20

n = len(posts)
n_test = int(n * HOLDOUT)
n_train = n - n_test

print "{} questions -- {} training -- {} test".format(n, n_train, n_test)

ids = posts.keys()

train_ids = ids[:n_train]
test_ids = ids[n_train:]

#print train_ids

train_titles = [posts[i]["title"] for i in train_ids]
test_titles = [posts[i]["title"] for i in test_ids]

#print train_titles[0:5]
#print test_titles[0:5]

train_labels = [(posts[i]["day"][1] - posts[i]["day"][2]) > CUTOFF for i in train_ids]
test_labels = [(posts[i]["day"][1] - posts[i]["day"][2]) > CUTOFF for i in test_ids]

#print train_labels[0:5]
#print test_labels[0:5]

print "{} training questions above cutoff".format(len(filter(None, train_labels)))
print "{} test questions above cutoff".format(len(filter(None, test_labels)))

vect = CountVectorizer()
tfidf = TfidfTransformer()
#clf = OneVsRestClassifier(LinearSVC())
clf = OneVsRestClassifier(SGDClassifier())

train_docs = vect.fit_transform(train_titles)
train_docs = tfidf.fit_transform(train_docs)
clf.fit(train_docs, train_labels)

test_docs = vect.transform(test_titles)
test_docs = tfidf.transform(test_docs)
predicted = clf.predict(test_docs)

print test_docs.shape

#print list(predicted)

n_predict_true = sum(int(p) for p in predicted)
n_predict_false = sum(1 - int(p) for p in predicted)

print "Prediction: {} above cutoff, {} below".format(n_predict_true, n_predict_false)

n_correct = sum(int(p == l) for p,l in zip(predicted,test_labels))
print n_correct / len(test_labels), "\"accuracy\""
