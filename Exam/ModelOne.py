#-*- coding: UTF-8 -*-
from __future__ import division
import codecs
import random

signsAllowed = map(chr, range(97, 123)) # az
signsAllowed += map(chr, range(65, 91)) # AZ
signsAllowed += [u'æ', u'ø', u'å', u'Æ', u'Ø', u'Å']
signsAllowed += [',', '.', ' ']


class ModelOne():
    dict = {}
    signs = {}
    total = 0

    def __init__(self):
        readfile = codecs.open("ugeseddel_data.txt", "r", "utf-8")
        lines = readfile.readlines()
        for line in lines:
            # Removes \n and other symbols for text formatting
            words = line.strip()
            # Splits the lines into arrays of words, splitting at whitespaces
            for sign in words:
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

    def generate_string(self, n):
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