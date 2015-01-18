#-*- coding: UTF-8 -*-
from __future__ import division
from SignsAllowed import signsAllowed
import codecs
import random
import re
import numpy as np

# A node knows the chances of the next encountering every other node as the next node from itself
class Node():
    def __init__(self, words):
        self.next = {}
        for word in words:
            self.next[word] = 0

    def __getitem__(self, item):
        return self.next[item]

    def getnext(self):
        i = random.random()

        s = 0

        for word in self.next.keys():
            s += self.next[word]
            if i <= s:
                return word
        return None

    def __setitem__(self, key, value):
        self.next[key] = value

    def items(self):
        return self.next.items()


# Every node possible needs to representated
class ModelThree():

    dict = {}

    def __init__(self):
        self.dict = {}
        self.text = ""
        self.starting = {}
        self.total = 0
        self.vocabulary = {}

    def readfile(self):
        self.vocabulary = {}
        readfile = codecs.open("ugeseddel_data.txt", "r", "utf-8")
        lines = readfile.readlines()
        for line in lines:
            line = re.sub(u'[^A-ZÆØÅa-zæøå0-9 ]+', '', line)

            words = line.split(" ")
            self.text += " ".join(words)
            for word in words:
                if word != u"":
                    if word in self.vocabulary.keys():
                        self.vocabulary[word] += 1
                        self.total += 1
                    else:
                        self.vocabulary[word] = 1
                        self.total += 1
        for word in self.vocabulary.keys():
            self.dict[word] = Node(self.vocabulary.keys())

    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def findmatches(self, word, next):
        t = word+" "+next
        regex = re.compile(t)
        return regex.findall(self.text)

    def calculatespread(self):
#        import time
        print "Processing ", len(self.dict.keys()), " words (Be patient!)"

        for word1 in self.dict.keys():
            start = time.time()
            occurences = 0
    # PROCESSOR EXPENSIVE
    #        for k, _ in self.dict.iteritems():
    # MEMORY EXPENSIVE
            for k in self.dict[word1].next.keys():
                occurence = len(self.findmatches(word1, k))
                if occurence != 0:
                    self.dict[word1][k] = occurence
                    occurences += occurence
                else:
                    self.dict[word1][k] = 0
            if occurences > 0:
# PROCESSOR EXPENSIVE
#                for k, _ in self.dict[word1].next.iteritems():
# MEMORY EXPENSIVE
                for k in self.dict[word1].next.keys():
                    self.dict[word1][k] /= occurences
            end = time.time()
            print "time spent : " + str(end - start)

#                self.dict[word1] = {k: v / occurences for k, v in self.dict[word1].items()}
#                for word2 in keys:
#                    self.dict[word1][word2] /= occurences

    def getstart(self):
        chance = 0
        for word in self.dict.keys():
            try:
                chance += self.vocabulary[word] / self.total
                self.starting[chance] = word
            except KeyError:
                # Symbol didn't excist, so skipping
                continue

        i = random.random()
        keys = self.starting.keys()
        keys.sort()
        for key in keys:
            if i < key:
                return self.starting[key]

    def generatestring(self, n):
        st = [self.getstart()]
        last = st[0]
        for _ in range(n-1):
            last = self.dict[last].getnext()
            if not last:
                # There's no place to go, word has no followers, finding new starting word
                last = self.getstart()
#                break
            st.append(last)
        return " ".join(st)

    def matrixit(self):
        keys = self.vocabulary.keys()
        keys.sort()
        m = np.zeros((len(keys), len(keys)), dtype=float)
        for i in np.arange(len(keys)):
            for j in np.arange(len(keys)):
#                print keys[i], keys[j]
                m[i][j] = len(self.findmatches(keys[i], keys[j]))
            print ".",
        print m
#        matrix = np.random.randint(100, size=(len(keys), len(keys)))