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
with open('res/corpus.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    raw_instances = [(row['url'], row['comment'], row['category']) for row in reader]
    for instance in raw_instances:
        url, comment, category = instance
        if url not in deviations:
            deviations[url] = ([], category)
        comments, _ = deviations[url]
        comments.append(comment)

categories = []
comments = []
for _, deviation in deviations.items():
    comment, category = deviation
    comments.append(' '.join(comment))
    categories.append(category)

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

print("Random Forest")
print(metrics.accuracy_score(categories, predicted))
