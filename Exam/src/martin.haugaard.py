#-*- coding: UTF-8 -*-
from __future__ import division
import matplotlib.pyplot as plt
from ModelOne import *
from ModelTwo import *
from ModelThree import *
__author__ = 'Martin Haugaard, cdl966'


if __name__ == "__main__":

    print "Generating Object for ModelOne, single signs"
    m1 = ModelOne()
    # Shows the histogram of ModelOne.
    plt.figure("ModelOne Histogram")
    plt.xticks(xrange(len(m1.k)), m1.k)
    plt.plot(m1.gethist())
    plt.xlim([0, len(m1.k)])
    plt.show()
    print "Randomly generated text, of length 10: ", m1.generatestring(10)
    print "Generating 1000 long random text, saves as model1.txt"
    f = open('model1.txt', 'w')
    st = m1.generatestring(1000)
    f.write(st.encode('utf8'))
    f.close()

    print "\n####\n"

    print "Generating Object for ModelTwo, paired signs"
    m2 = ModelTwo()
    print "Reading the filedata"
    m2.readfile()
    print "Preparing the historgram for ModelTwo"
    plt.figure("ModelTwo Histogram")
    plt.xticks(xrange(len(m2.k)), m2.k)
    plt.plot(m2.gethist())
    plt.xlim([0, len(m2.k)])
    plt.show()

    # Left axis is the start value, right axis is the end value.
    print "Preparing the Transition table for ModelTwo"
    plt.figure("Transition Table for ModelTwo")
    plt.yticks(xrange(len(m2.k)), m2.k)
    plt.xticks(xrange(len(m2.k)), m2.k)
    plt.imshow(m2.matrix)
    plt.show()
    print "Randomly generated text, of length 10: ", m2.generatestring(10)
    print "Generating 1000 long random text, saves as model2.txt"
    f = open('model2.txt', 'w')
    st = m2.generatestring(1000)
    f.write(st.encode('utf8'))
    f.close()

    print "\n####\n"

    print "Generating Object for ModelThree, paired words"
    mt = ModelThree()
    print "Reading the filedata"
    mt.readfile()
    print "Preparing the histogram for ModelThree"
    plt.figure("ModelThree Histogram")
    # Too many words to safely print
#    plt.xticks(xrange(len(mt.k)), mt.k)
    plt.plot(mt.gethist())
    plt.xlim([0, len(mt.k)])
    plt.show()

    # Left axis is the start value, right axis is the end value.
    print "Preparing the Transition table for ModelThree"
    plt.figure("Transition Table for ModelThree")
    # Once again, too many for this to make sense.
#    plt.yticks(xrange(len(mt.k)), mt.k)
#    plt.xticks(xrange(len(mt.k)), mt.k)
    plt.imshow(mt.matrix)
    plt.show()
    print "Randomly generated text, of length 10: ", mt.generatestring(10)
    # Remove comments if you want to redo this, commented out to save time when testing
    print "To save time, ModelThree will not generate 1000 word pairings here, remove comments in code to run"
#    print "Generating 1000 long random text, saves as model3.txt"
#    print "Please wait, this may take a while"
#    f = open('model3.txt', 'w')
#    st = mt.generatestring(1000)
#    f.write(st.encode('utf8'))
#    f.close()

    # TESTING BEGINS HERE
    print "\n###\nEntering Test Section:"
    """
    Jeg forventer at alle mine tre modeller, summer deres sandsynligheder til enten 1.0, eller 0.0.
    Altså skal alle forbindelser, fra et ord eller symbol, til alle alle de andre, enten være komplet (1.0) i det tilfælde
    hvor der er en forbindelse, eller alternativt nul, hvis der ikke findes en forbindelse.
    På samme måde, i første model, skal samtlige chancer gerne summes til 1.0. Da ethvert random.random() skal resultere i
    et symbol. Det tester jeg for efterfølgende
    """
    # Check the sum of all chances in ModelOne
    chance = sum(m1.dict.values())
    print "ModelOne spread sums to 1.0 ==", chance, float('%.3g' % chance) == 1.000

    def testMatrix(m):
        """
        Helper function for testing the matrix in ModelTwo and ModelThree
        """
        print "Testing the spread matrix:"
        for i in m.matrix:
            if float('%.3g' % sum(i)) != 1.000 and sum(i) != 0:
                print "The spread is not as expected", sum(i)
                return
        print "Matrix is acceptable"
    testMatrix(m2)
    testMatrix(mt)

    print "Reading file: simpletext.txt"
    # As the code in ModelTwo and ModelThree is basically the same, I will refrain from doing redundant work
    testM = ModelThree()
    testM.readfile("simpletext.txt")
    print "Generate new string"
    st = testM.generatestring(10)
    print "Length of a 10 words is 10", len(st.split(" ")) == 10
    # Provided the textfile has two words, text is generated, every time a 'dead end' is found, where no logical
    # move can be made, a new request for a starting point is made, and the process continues from there
    for _ in range(100):
        sign = testM.gennext(u'a')
        if not (sign == u'c' or sign == u'd'):
            print "Error found in the sequence.. has it been changed?", sign
    print "If no errors printed, then successfully predicted next sign, 100 times"
