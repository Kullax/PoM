#-*- coding: UTF-8 -*-
from __future__ import division
import codecs
import random
import re
import numpy as np
__author__ = 'Martin Haugaard, cdl966'


class ModelThree():
    """
    Basic model for determining word pairings from a given string, which then allows generation of a new string which may
    or may not make some sense
    """

    def __init__(self):
        self.dict = {}
        self.starting = {}
        self.total = 0
        self.vocabulary = {}
        self.k = []
        # Empty array
        self.matrix = np.array(())

    def readfile(self, f="ugeseddel_data.txt"):
        """
        Read a file, feeding the object with information needed to generate new sequences
        :param f: optional filepath, if left empty, default is used
        """
        readfile = codecs.open(f, "r", "utf-8")
        lines = readfile.readlines()

        last = u""
        for line in lines:
            line = re.sub(u'[^A-ZÆØÅa-zæøå0-9 ]+', '', line)
            words = line.split(" ")
            for word in words:
                if word != u"":
                    self.total += 1
                    if word in self.vocabulary:
                        self.vocabulary[word] += 1
                    else:
                        self.vocabulary[word] = 1
                    if last == u"":
                        last = word
                    else:
                        if (last, word) in self.dict:
                            self.dict[last, word] += 1
                        else:
                            self.dict[last, word] = 1
                    last = word

        # Last word will have no matches, so it's "forgotten" again
        self.vocabulary[last] -= 1
        self.k = self.vocabulary.keys()
        self.matrix = np.zeros((len(self.vocabulary), len(self.vocabulary)))
        for i in xrange(len(self.vocabulary)):
            for j in xrange(len(self.vocabulary)):
                if (self.k[i], self.k[j]) in self.dict:
                    self.matrix[i][j] = self.dict[self.k[i], self.k[j]] / self.vocabulary[self.k[i]]

    def gethist(self):
        """
        Returns a list, which can be used to generate a histogram of the object
        :return: a list of floats
        """
        list = np.zeros(len(self.k))
        for i in xrange(len(self.k)):
            list[i] += self.vocabulary[self.k[i]] / self.total
        return list


    def getstart(self):
        """
        Randomly picks a starting word, the pick is influenced by the occurences of the words in the original text
        :return: a random word from the original text
        """
        chance = 0
        r = random.random()
        for i in xrange(len(self.vocabulary)):
            chance += self.vocabulary[self.k[i]] / self.total
            if r <= chance:
                return self.k[i]
        print "No start found, trying again"
        return self.getstart()

    def gennext(self, n):
        """
        Given an input, determines the next word in the sequence, if no possible next word is found, a new one
        is found using getstart()
        :param n: current sign
        :return: next sign
        """
        chance = 0
        r = random.random()
        for i in xrange(len(self.vocabulary)):
            chance += self.matrix[self.k.index(n)][i]
            if r <= chance:
                return self.k[i]

    def generatestring(self, n):
        """
        Uses helper function getstart and gennext to put together a sequence of matching words. Should the sequence have
        a word with no possible next word, a new word is found from getstart, and the sequence continues.
        :param n: length of sequence to be generated
        :return: a randomly generated sequence of words, of length n
        """
        last = self.getstart()
        st = [last]
        for _ in range(n-1):
            sign = self.gennext(last)
            if sign is None:
                sign = self.getstart()
            st.append(sign)
            last = sign
        return " ".join(st)