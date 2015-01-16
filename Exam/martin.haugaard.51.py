#-*- coding: UTF-8 -*-
from ModelOne import *

# Definition of allowed signs for the text, being the danish alphabet a-zA-Z and , . and whitespace.as
# This means signs like, for example é will be ignored.



if __name__ == "__main__":
    m1 = ModelOne()
    print m1.generate_string(100)
    print "P of æ:\t\t\t", m1.getprob(u'æ')
    print "P of '_':\t\t", m1.getprob(' ')
