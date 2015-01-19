#-*- coding: UTF-8 -*-
from __future__ import division
import codecs
import random
import numpy as np
from SignsAllowed import signsAllowed
__author__ = 'Martin Haugaard, cdl966'


class ModelTwo():
    """
    Basic model for determining sign pairings from a given string, which then allows generation of a new series of signs
    which is then influenced by the original sequence
    """

    def __init__(self):
        self.dict = {}
        self.starting = {}
        self.total = 0
        self.signs = {}
        self.k = []
        for sign in signsAllowed:
            self.signs[sign] = 0
        self.k = self.signs.keys()

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
            for sign in line:
                if sign in signsAllowed:
                    self.total += 1
                    if last == u"":
                        last = sign
                    else:
                        if (last, sign) in self.dict:
                            self.dict[last, sign] += 1
                        else:
                            self.dict[last, sign] = 1
                        self.signs[last] += 1
                        last = sign
        # Last sign will have no matches, so it's "forgotten" again
        self.signs[last] -= 1
        # Time to make the transition matrix, which connects the different signs with each other
        self.matrix = np.zeros((len(self.k), len(self.k)))
        for i in xrange(len(self.k)):
            chance = 0
            for j in xrange(len(self.k)):
                if (self.k[i], self.k[j]) in self.dict:
                    chance += self.dict[self.k[i], self.k[j]] / self.signs[self.k[i]]
                    self.matrix[i][j] = self.dict[self.k[i], self.k[j]] / self.signs[self.k[i]]

    def gethist(self):
        """
        Returns a list, which can be used to generate a histogram of the object
        :return: a list of floats
        """
        list = np.zeros(len(self.k))
        for i in xrange(len(self.k)):
            list[i] += self.signs[self.k[i]] / self.total
        return list


    def getstart(self):
        """
        Randomly picks a starting sign, the pick is influenced by the occurences of the signs in the original text
        :return: a random sign from the original text
        """
        chance = 0
        r = random.random()
        for i in xrange(len(self.signs)):
            chance += self.signs[self.k[i]] / self.total
            if r <= chance:
                return self.k[i]
        print "No start found, trying again"
        return self.getstart()

    def gennext(self, n):
        """
        Given an input, determines the next sign in the sequence, if no possible next sign is found, a new one
        is found using getstart()
        :param n: current sign
        :return: next sign
        """
        chance = 0
        r = random.random()
        for i in xrange(len(self.signs)):
            chance += self.matrix[self.k.index(n)][i]
            if r <= chance:
                return self.k[i]

    def generatestring(self, n):
        """
        Uses helper function getstart and gennext to put together a sequence of matching signs. Should the sequence have
        a sign with no possible next sign, a new sign is found from getstart, and the sequence continues.
        :param n: length of sequence to be generated
        :return: a randomly generated sequence of signs, of length n
        """
        last = self.getstart()
        st = last
        for _ in range(n-1):
            sign = self.gennext(last)
            # In case of no next, means we have hit a dead end, so now we start over somewhere else
            if sign is None:
                sign = self.getstart()
            st += sign
            last = sign
        return st