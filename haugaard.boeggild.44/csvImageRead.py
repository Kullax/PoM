# -*- coding: utf-8 -*-
'''
Created on Oct 10, 2014

@author: Mossa og Katrine
'''
import csv


def csvImageRead(sFileName):
    """ Retunere billedets pixels i en liste af lister fra filen sFileName.

    Formattet "liste af lister" er nøje beskrevet i ugeseddel 8, formel (2).
    """
    mImageList = []
    try:
        with open(sFileName, "rb") as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                floats = [float(x) for x in row]
                mImageList.append(floats)

            return mImageList

    except IOError as e:
        print u"Der er opstået en fejl! Findes filen?"
        print e
    finally:
        return mImageList

if __name__ == "__main__":
    #Tester om metoden håndtere ikke-eksisterende file
    print csvImageRead("Findes_ikke.csv")
