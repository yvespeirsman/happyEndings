__author__ = 'yves'

import epub
import re
import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from SentiWordNet import SentiWordNet

WINDOW_SIZE = 5000
BOOK = "pg730"

senti = SentiWordNet.SentiWordNet()
sentiment = senti.reduce()

book = epub.open_epub('/home/yves/Documents/projects/happyEndings/'+BOOK+'.epub')
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
allScores = []
numWords = 0
for sentence in allSentences:
    pos = nltk.pos_tag(sentence)
    for (word, tag) in pos:
        numWords += 1
        lem = tag[0].lower()
        x = word.lower()

        wordScore = 0
        if lem in ["a","r","v","n"]:
            lemma = lemmatizer.lemmatize(word.lower(),tag[0].lower())
            word = lemma + "/" + tag[0].lower()
            if sentiment.has_key(word):
                wordScore = sentiment[word]

            scores.append(wordScore)
            if len(scores) > WINDOW_SIZE:
                scores = scores[1:]
            curScore = sum(scores)/float(len(scores))
            allScores.append([numWords,curScore])

o = open('/home/yves//PycharmProjects/HappyEndings/static/'+BOOK+'-smooth-'+str(WINDOW_SIZE)+'-narv.tsv',"w")
for (w,s) in allScores:
    o.write(str(w) + "\t" + str(s) + "\n")
o.close()


print scores
