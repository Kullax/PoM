#-*- coding: UTF-8 -*-
from __future__ import division
from SignsAllowed import signsAllowed
import codecs
import random



class ModelOne():

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
                        self.total += 1
                    # first time sign is seen, register it
                    else:
                        self.signs[sign] = 1
                        self.total += 1

        # keys now hold all the signs seen
        keys = self.signs.keys()
        # sorts it, so order is the same for future references, where it also gets sorted
        keys.sort()
        # p is the total procentage of seeing a sign, or any before it.
        p = 0
        for key in keys:
            # if its the last key, the procentage should be 100%
            if key == keys[len(keys)-1]:
                p = 1
            else:
                p += self.signs[key] / self.total
            self.dict[p] = key

    def generatestring(self, n):
        st = ""
        for _ in range(n):
            i = random.random()
            keys = self.dict.keys()
            # need the keys to be ordered, for the next part
            keys.sort()
            for key in keys:
                if i <= key:
                    st += self.dict[key]
                    break
        return st

    def getprob(self, k):
        if k in signsAllowed:
            try:
                s = self.signs[k] / self.total
                return s
            except:
                return 0
        return 0