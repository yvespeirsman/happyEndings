__author__ = 'yves'

import re

class SentiWordNet():

    def __init__(self):
        d = {}
        i = open("/usr/local/SentiWordNet/SentiWordNet_3.0.0_20130122.txt")
        for line in i:
            if not line[0]== "#":
                if len(line.strip().split("\t")) == 6:
                    (POS, ID, PosScore, NegScore, SynsetTerms, Gloss) = line.strip().split("\t")
                    for term in SynsetTerms.split():
                        word = term.split("#")[0]
                        word = re.sub("_", " ", word)
                        wordPos = word + "/" + POS
                        if not d.has_key(wordPos):
                            d[wordPos] = {}
                            d[wordPos]["pos"] = []
                            d[wordPos]["neg"] = []

                        d[wordPos]["pos"].append(float(PosScore))
                        d[wordPos]["neg"].append(float(NegScore))

        i.close()
        self.dictionary = d

    def reduce(self):
        newD = {}
        for word in self.dictionary:
            allPos = self.dictionary[word]["pos"]
            allNeg = self.dictionary[word]["neg"]
            avgPos = sum(allPos)/len(allPos)
            avgNeg = sum(allNeg)/len(allNeg)

            newD[word] = avgPos - avgNeg
        return newD



