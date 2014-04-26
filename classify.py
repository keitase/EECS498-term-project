from __future__ import division

from postdata import posts as a_posts
from balanced_postdata import posts as b_posts
from timeweighted_postdata import posts as t_posts
from balanced_timeweighted_postdata import posts as bt_posts

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC

import argparse

parser = argparse.ArgumentParser(description='Predict successfull reddit posts')
parser.add_argument('--cutoff', dest='cutoff', type=int, default=100,
                    help="Predict posts with this many or more upvotes")
parser.add_argument('--dat', dest='dat', action='store_const',
                    const=True, default=False,
                    help="Print output in a gnuplot-friendly format")
parser.add_argument('--posts', dest='posts', type=str, default="a",
                    help="Train on: a,b,t,bt")
parser.add_argument('--cheat', dest='cheat', action='store_const',
                    const=True, default=False,
                    help="Use upvotes to predict upvotes...")

args = parser.parse_args()

CUTOFF = args.cutoff
HOLDOUT = .20

if args.posts == "a":
    posts = a_posts
elif args.posts == "b":
    posts = b_posts
    #exit("This is not set up to handle balanced datasets.")
elif args.posts == "t":
    posts = t_posts
elif args.posts == "bt":
    posts = bt_posts
    #exit("This is not set up to handle balanced datasets.")

def has_title(p):
    return "title" in p
posts = {k: post for k,post in posts.iteritems() if has_title(post)}

n = len(posts)
n_test = int(n * HOLDOUT)
n_train = n - n_test

ids = posts.keys()

train_ids = ids[:n_train]
test_ids = ids[n_train:]

if args.cheat:
    train_ds = [(posts[i]["day"][1] - posts[i]["day"][2]) for i in train_ids]
    train_hs = [(posts[i]["hour"][1] - posts[i]["hour"][2]) for i in train_ids]

    cut_hours = [h for h,d in zip(train_hs, train_ds) if d > CUTOFF]
    cut_hr = sorted(cut_hours)[10]

    test_ds = [(posts[i]["day"][1] - posts[i]["day"][2]) for i in test_ids]
    test_hs = [(posts[i]["hour"][1] - posts[i]["hour"][2]) for i in test_ids]

    true_pos = len([1 for d,h in zip(test_ds,test_hs) if d > CUTOFF and h >= cut_hr])
    false_pos = len([1 for d,h in zip(test_ds,test_hs) if d <= CUTOFF and h >= cut_hr])
    false_neg = len([1 for d,h in zip(test_ds,test_hs) if d > CUTOFF and h < cut_hr])
    true_neg = len([1 for d,h in zip(test_ds,test_hs) if d <= CUTOFF and h < cut_hr])

    print n_test
    print true_pos,false_pos,false_neg,true_neg
    print "Recall: {} -- Precision: {}".format(
            true_pos / (true_pos + false_neg),
            true_pos / (true_pos + false_pos))
    
    #print min(cut_hours)
    #print min(hr_scores)
    #print sum(cut_hours) / len(cut_hours)
    #print sum(hr_scores) / len(hr_scores)
    exit(0)

#print train_ids

train_titles = [posts[i]["title"] for i in train_ids]
test_titles = [posts[i]["title"] for i in test_ids]

#print train_titles[0:5]
#print test_titles[0:5]

train_labels = [(posts[i]["day"][1] - posts[i]["day"][2]) > CUTOFF for i in train_ids]
test_labels = [(posts[i]["day"][1] - posts[i]["day"][2]) > CUTOFF for i in test_ids]

#print train_labels[0:5]
#print test_labels[0:5]

##############################################################################
# Looking for 10 lines of code?

vect = CountVectorizer()
tfidf = TfidfTransformer()
#clf = OneVsRestClassifier(LinearSVC())
#clf = OneVsRestClassifier(SGDClassifier())
clf = OneVsRestClassifier(SGDClassifier(class_weight="auto"))

train_docs = vect.fit_transform(train_titles)
train_docs = tfidf.fit_transform(train_docs)
clf.fit(train_docs, train_labels)

test_docs = vect.transform(test_titles)
test_docs = tfidf.transform(test_docs)
predicted = clf.predict(test_docs)

# Close enough?
##############################################################################

#print list(predicted)

n_predict_true = sum(int(p) for p in predicted)
n_predict_false = sum(1 - int(p) for p in predicted)

n_true_pos = sum(1 for p,l in zip(predicted,test_labels) if p == 1 and l == 1)
n_true_neg = sum(1 for p,l in zip(predicted,test_labels) if p == 0 and l == 0)
n_false_pos = sum(1 for p,l in zip(predicted,test_labels) if p == 1 and l == 0)
n_false_neg = sum(1 for p,l in zip(predicted,test_labels) if p == 0 and l == 1)
#n_correct = sum(1 for p,l in zip(predicted,test_labels) if p == l)
n_correct = n_true_pos + n_true_neg

n_test = len(test_labels)
n_above = len(filter(None, test_labels))
n_below = n_test - n_above

if args.dat:
    print "a{}\t{}\t0\t0\t{}".format(CUTOFF, n_below, n_above)
    print "p{}\t{}\t{}\t{}\t{}".format(
            CUTOFF, n_true_neg, n_false_neg, n_false_pos, n_true_pos)
else:
    print "{} questions -- {} training -- {} test".format(n, n_train, n_test)

    print "{} training questions above cutoff".format(
            len(filter(None, train_labels)))
    print "{} test questions above cutoff".format(
            len(filter(None, test_labels)))

    print test_docs.shape

    print "Prediction: {} above cutoff, {} below".format(
            n_predict_true, n_predict_false)
    print "{} false positives, {} false negatives".format(n_false_pos, n_false_neg)
    print "Recall: {} -- Precision: {}".format(
            n_true_pos / n_above, n_true_pos / (n_true_pos + n_false_pos))

    #print n_correct / len(test_labels), "accuracy"

#print clf.get_params()
