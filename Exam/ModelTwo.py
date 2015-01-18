#-*- coding: UTF-8 -*-
from __future__ import division
from SignsAllowed import signsAllowed
import codecs
import random
import re


# A node knows the chances of the next encountering every other node as the next node from itself
class Node():

    def __init__(self):
        self.next = {}
        for sign in signsAllowed:
            self.next[sign] = 0

    def __getitem__(self, item):
        return self.next[item]

    def getnext(self):
        i = random.random()

        s = 0
        for sign in signsAllowed:
            s += self.next[sign]
            if i <= s:
                return sign
        return None

    def __setitem__(self, key, value):
        self.next[key] = value



# Every node possible needs to representated
class ModelTwo():

    dict = {}

    def __init__(self):
        self.dict = {}
        self.text = ""
        self.starting = {}
        self.signs = {}
        self.total = 0
        for sign in signsAllowed:
            self.dict[sign] = Node()

    def readfile(self):
        readfile = codecs.open("ugeseddel_data.txt", "r", "utf-8")
        lines = readfile.readlines()
        for line in lines:
            for sign in line:
                # if sign is a newline, process it as if it was a whitespace
                if sign == '\n':
                    sign = ' '
                # if sign is legal continue, else skip
                if sign in signsAllowed:
                    self.text += sign
                    # if sign already seen, increment number of times seen
                    if sign in self.signs:
                        self.signs[sign] += 1
                        self.total += 1
                    # first time sign is seen, register it
                    else:
                        self.signs[sign] = 1
                        self.total += 1

    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def findmatches(self, sign, next):
        if next == ".":
            next = '\.'
        if sign == ".":
            sign = '\.'
        t = sign+next
        return [m.start() for m in re.finditer('(?=%s)' % t, self.text)]

    def calculatespread(self):
        for sign1 in signsAllowed:
            occurences = 0
            for sign2 in signsAllowed:
                occurence = len(self.findmatches(sign1, sign2))
                self.dict[sign1][sign2] = occurence
                occurences += occurence
            if occurences > 0:
                for sign2 in signsAllowed:
                    self.dict[sign1][sign2] /= occurences

    def getstart(self):
        chance = 0
        for sign in signsAllowed:
            try:
                chance += self.signs[sign] / self.total
                self.starting[chance] = sign
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
        st = self.getstart()
        last = st
        for _ in range(n-1):
            last = self.dict[last].getnext()
            st += last
        return st
