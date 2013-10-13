__author__ = 'yves'

import epub
import re
import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from SentiWordNet import SentiWordNet

senti = SentiWordNet.SentiWordNet()
sentiment = senti.reduce()

book = epub.open_epub('/home/yves/Documents/projects/happyEndings/pg1400.epub')
allSentences = []

w = 0
for item in book.opf.manifest.values():
    # read the content
    data = book.read_item(item)
    for line in data.split("\n"):
        if re.search("^<p", line):
            line = re.sub("<.*?>","", line)
            sentences = [word_tokenize(t) for t in sent_tokenize(line)]
            for sentence in sentences:
                allSentences.append(sentence)
            w += len(line.split())

scores = []
numWords = 0
totScore = 0
for sentence in allSentences:
    pos = nltk.pos_tag(sentence)
    for (word, tag) in pos:
        numWords += 1
        lem = tag[0].lower()
        x = word.lower()
        if lem in ["a","r","v","n"]:
            lemma = lemmatizer.lemmatize(word.lower(),tag[0].lower())
            word = lemma + "/" + tag[0].lower()
            if sentiment.has_key(word):
                totScore += sentiment[word]
        if numWords % 2000 == 0:
            print numWords, totScore
            scores.append([numWords,totScore])
            totScore = 0

o = open('/home/yves/Documents/projects/happyEndings/pg1400-2000.tsv',"w")
for (w,s) in scores:
    o.write(str(w) + "\t" + str(s) + "\n")
o.close()


print scores
