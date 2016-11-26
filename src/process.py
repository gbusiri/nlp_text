import csv
import utils
import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import RandomForestClassifier

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
X = tfidf_vectorizer.fit_transform(comments)
print(X.todense())
y = categories
print(X)
print(y)

classifier = RandomForestClassifier(n_estimators=10, max_depth=None,
                                    min_samples_split=2, random_state=0)

print("Classifying using Random Forest...")
predicted = cross_val_predict(classifier, X, y, cv=10)

for i in range(len(categories)):
    if categories[i] == 'Photography':
        print(comments[i])
        print(categories[i] + ' --- ' + predicted[i])

print("Random Forest")
print(metrics.accuracy_score(categories, predicted))
