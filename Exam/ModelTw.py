#-*- coding: UTF-8 -*-
from __future__ import division
from SignsAllowed import signsAllowed
import codecs
import random
import re
import numpy as np

class ModelTw():

    def __init__(self):
        self.dict = {}
        self.starting = {}
        self.total = 0
        self.signs = {}
        self.k = []
        for sign in signsAllowed:
            self.signs[sign] = 0
        self.k = self.signs.keys()
#        self.k.sort()

        self.matrix = np.array(())

    def readfile(self):
        readfile = codecs.open("ugeseddel_data.txt", "r", "utf-8")
        lines = readfile.readlines()

        last = u""
        for line in lines:
            for sign in line:
#                if sign == u'\n':
#                    sign == ''
                if sign in signsAllowed:
                    self.total += 1
#                    self.signs[sign] += 1
                    if last == u"":
                        last = sign
                    else:
#                        if last == u'\n':
#                            print "EOL!"
#                        else:
#                            print ".",
                        if (last, sign) in self.dict:
                            self.dict[last, sign] += 1
                        else:
                            self.dict[last, sign] = 1
                        self.signs[last] += 1
                        last = sign
        self.matrix = np.zeros((len(self.k), len(self.k)))
        for i in xrange(len(self.k)):
            chance = 0
            for j in xrange(len(self.k)):
                if (self.k[i], self.k[j]) in self.dict:
                    chance += self.dict[self.k[i], self.k[j]] / self.signs[self.k[i]]
                    self.matrix[i][j] = self.dict[self.k[i], self.k[j]] / self.signs[self.k[i]]

    def getstart(self):
        chance = 0
        r = random.random()
        for i in xrange(len(self.signs)):
            chance += self.signs[self.k[i]] / self.total
            if r <= chance:
                return self.k[i]

    def gennext(self, n):
        chance = 0
        r = random.random()
        for i in xrange(len(self.signs)):
            chance += self.matrix[self.k.index(n)][i]
            if r <= chance:
                return self.k[i]

#        r = random.random()
#        for i in xrange(len(self.vocabulary)):
#            if r <= sum(self.matrix[self.k.index(n)][:i+1]):
#                return self.k[i]
