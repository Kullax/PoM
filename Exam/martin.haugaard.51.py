
#-*- coding: UTF-8 -*-
from __future__ import division
from ModelOne import *
from ModelTwo import *
from ModelThree import *
import time

import matplotlib.pyplot as plt
from ModelTw import *
from ModelT import *

if __name__ == "__main__":
#    mt = ModelT()
#    mt.readfile()
#    start = mt.getstart()
#    print start,
#    for i in range(10):
#        start = mt.gennext(start)
#        print start,


    m2 = ModelTw()
    m2.readfile()

    plt.figure()
#    plt.plot(mt.matrix)
    plt.imshow(m2.matrix)
    plt.xlabel("".join(m2.k))
    plt.show()

    for i in m2.matrix:
        if float('%.3g' % sum(i)) != 1.000:
            print "NEJ DA!"



#    m = np.zeros((61, 61))
#    m[30][0] = 255
#    plt.figure()
#    plt.imshow(m)
#    plt.show()
#    for i in xrange(len(m2.matrix)):
#        for j in xrange(len(m2.matrix)):
#            print sum(m2.matrix[i][:j+1])
#            m[i][j] = sum(m2.matrix[i][:j+1])
#        print sum(m[i])



#    start = time.time()
#    print "New Model, 3"
#    m3 = ModelThree()
#    print "Read file"
#    m3.readfile()
#    print "Matrix it"
#    m3.matrixit()
#    print "Calculate spread"
#    m3.calculatespread()
#    print "Generate file"
#    print m3.generatestring(1000)
"""
    m1 = ModelOne()
    print m1.generatestring(100)
    print "P of æ:\t\t\t", m1.getprob(u'æ')
    print "P of '_':\t\t", m1.getprob(' ')

    m2 = ModelTwo()
    print "Reading file"
    m2.readfile()
    print "Calculating sign pair chances"
    m2.calculatespread()
    print "Generating random text"
    print m2.generatestring(250)
    print "Generating random text"
    print m2.generatestring(250)
    print "Generating random text"
    print m2.generatestring(250)
"""
