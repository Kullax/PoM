#-*- coding: UTF-8 -*-
from __future__ import division
import codecs
import random
from SignsAllowed import signsAllowed
import numpy as np
__author__ = 'Martin Haugaard, cdl966'


class ModelOne():
    """
    Simple Object for generating a random sequence of signs, given an original text as a source of influence
    """

    def __init__(self):
        self.dict = {}
        self.signs = {}
        self.total = 0

        readfile = codecs.open("ugeseddel_data.txt", "r", "utf-8")
        lines = readfile.readlines()
        for line in lines:
            # Splits the lines into arrays of words, splitting at whitespaces
            for sign in line:
                if sign == '\n':
                    sign = ' '
                # if sign is legal continue, else skip
                if sign in signsAllowed:
                    # if sign already seen, increment number of times seen
                    if sign in self.signs:
                        self.signs[sign] += 1
                    # first time sign is seen, register it
                    else:
                        self.signs[sign] = 1
                    self.total += 1
        # signs.keys now hold all the signs seen
        self.k = self.signs.keys()
        for key in self.k:
            # Set the chance that this key is found
            p = self.signs[key] / self.total
            self.dict[key] = p

    def generatestring(self, n):
        """
        Requests a sign for as many times as set in the parameter, n, and puts these together into a sequence of length
        n, and returns it
        :param n: number of signs needed
        :return: the new sequence of signs
        """
        st = ""
        # For each sign requested
        for _ in range(n):
            # random value, which gives location of sign we're looking for
            r = random.random()
            # Percentage chance that this is the sign we're looking for
            p = 0
            for key in self.k:
                # this sign's probability added to the previous probability
                p += self.dict[key]
                # if the randomly generated value is lower than the sum, we have our sign
                if r <= p:
                    # add the sign to the string, and break this inner loop
                    st += key
                    break
        # Return a now hopefully complete sequence of length n
        return st

    def gethist(self):
        """
        Generates a histogram, showcasing the chance of every sign in the model
        :return: a list of chances, order matching the signs in self.k
        """
        list = np.zeros(len(self.k))
        for i in xrange(len(self.k)):
            list[i] += self.dict[self.k[i]]
        return list