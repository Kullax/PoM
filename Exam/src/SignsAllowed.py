#-*- coding: UTF-8 -*-
__author__ = 'Martin Haugaard, cdl966'
#  Definition of allowed signs for the text, being the danish alphabet a-zA-Z and , . and whitespace.as
# This means signs like, for example é will be ignored.
signsAllowed = map(chr, range(97, 123)) # az
signsAllowed += map(chr, range(65, 91)) # AZ
signsAllowed += [u'æ', u'ø', u'å', u'Æ', u'Ø', u'Å']
signsAllowed += [',', '.', ' ']
