import csv
import pprint
import utils
import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.svm import LinearSVC

from sklearn import metrics

deviations = dict()
categories = []
comments = []
with open('res/corpus.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        categories.append(row['category'])
        comments.append(row['comment'])

tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(comments)

def benchmark(classifier, data, target):
    cls_name = type(classifier).__name__
    print("Classifying using {}...".format(cls_name))
    predicted = cross_val_predict(classifier, data, target, cv=10)

    print("{} Report".format(cls_name))
    print("===================")
    print(metrics.classification_report(target, predicted))

    pp = pprint.PrettyPrinter(indent=2)
    print("")
    print("Accuracy: {}".format(metrics.accuracy_score(target,predicted)))
    print("Confusion Matrix")
    print(metrics.confusion_matrix(target,predicted))
    print("===========")
    print("")

classifiers = [
    RandomForestClassifier(n_estimators=12, max_depth=None,
                           min_samples_split=2, random_state=0),
    OneVsOneClassifier(LinearSVC(random_state=2)),
    OneVsRestClassifier(LinearSVC(random_state=2)),
]

for classifier in classifiers:
    benchmark(classifier, tfidf, categories)
