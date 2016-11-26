import nltk
import csv
import utils

import nltk.corpus
dir(nltk.corpus)

texts = []


with open('res/corpus.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        texts.append(row['processed_text'])

print(texts)

for text in texts:
    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tags)
    print(text)
    print(tokens)
    print(tags)
    print(entities)
