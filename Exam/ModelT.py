#-*- coding: UTF-8 -*-
from __future__ import division
from SignsAllowed import signsAllowed
import codecs
import random
import re
import numpy as np

class ModelT():

    def __init__(self):
        self.dict = {}
#        self.text = ""
        self.starting = {}
        self.total = 0
        self.vocabulary = {}
        self.k = []
        # Empty array
        self.matrix = np.array(())
#        self.connection = {}

    def readfile(self):
        readfile = codecs.open("ugeseddel_data.txt", "r", "utf-8")
        lines = readfile.readlines()

        last = u""
        for line in lines:
            line = re.sub(u'[^A-ZÆØÅa-zæøå0-9 ]+', '', line)
            words = line.split(" ")
            for word in words:
                if word != u"":
                    self.total += 1
                    if word not in self.vocabulary:
                        self.vocabulary[word] = 1
                    else:
                        self.vocabulary[word] += 1
                    if last == u"":
                        last = word
                    else:
                        if (last, word) in self.dict:
                            self.dict[last, word] += 1
                        else:
                            self.dict[last, word] = 1
                    last = word
        self.k = self.vocabulary.keys()
        self.matrix = np.zeros((len(self.vocabulary), len(self.vocabulary)))
        for i in xrange(len(self.vocabulary)):
            for j in xrange(len(self.vocabulary)):
                if (self.k[i], self.k[j]) in self.dict:
                    self.matrix[i][j] = self.dict[self.k[i], self.k[j]] / self.vocabulary[self.k[i]]


    def getstart(self):
#        start = np.zeros(len(self.vocabulary))
        chance = 0
        r = random.random()
        for i in xrange(len(self.vocabulary)):
            chance += self.vocabulary[self.k[i]] / self.total
            if r <= chance:
                return self.k[i]

    def gennext(self, n):
        chance = 0
        r = random.random()
        for i in xrange(len(self.vocabulary)):
            chance += self.matrix[self.k.index(n)][i]
            if r <= chance:
                return self.k[i]

#        r = random.random()
#        for i in xrange(len(self.vocabulary)):
#            if r <= sum(self.matrix[self.k.index(n)][:i+1]):
#                return self.k[i]
