#-*- coding: UTF-8 -*-
from __future__ import division
import matplotlib.pyplot as plt
import sys
__author__ = 'Martin Simon Haugaard'


class Dataset():

    def __init__(self):
        """
        Initializes a new Dataset object
        """
        self.dataPoints = {}

    def __contains__(self, item):
        """
        checks if key i present in the dataPoints
        :param item: key value
        :return: boolean value
        """
        return self.dataPoints.__contains__(item)

    def __getitem__(self, key):
        """
        overwrites the dataset[key] operation
        """
        if self.dataPoints.__contains__(key):
            return self.dataPoints[key]
        raise KeyError("dataPoints does not contain keyvalue %d" % (key))

    def __setitem__(self, key, value):
        """
        overwrites the dataset[key] = value operation
        """
        self.dataPoints[key] = value

    def readDataPoints(self, filePath):
        """
        read from a filepath into the dataset
        the filePath must contain a series of number values, separated either by newlines or by commas.
        """
        f = open(filePath, 'r')
        lines = f.readlines()
        f.closed
        tokens = []
        for line in lines:
            tokens += line.split(',')
        if not len(tokens) % 2 == 0:
            raise ImportError("Cannot parse filedata, uneven number of inputs")
        for i in xrange(len(tokens)):
            # removing any white space in front or back of the object
            try:
                tokens[i] = float(tokens[i].strip())
            except:
                raise ValueError("Dataset expects all values to be single numbers, recieved %s" % tokens[i])
        # Data seems solid, time to parse it into the Dataset
        key = None
        for i in xrange(len(tokens)):
            if i % 2 == 0:
                key = tokens[i]
            else:
                self.dataPoints[key] = tokens[i]
                key = None

    def keys(self):
        """
        returns a list of keys for the dataset structure
        """
        return self.dataPoints.keys()

    def getminkey(self):
        """
        returns the lowest of the keys in the dataset
        """
        return min(self.dataPoints.keys())

    def getmaxkey(self):
        """
        returns the highest of the keys in the dataset
        """
        return max(self.dataPoints.keys())


class Regression():
    def __init__(self, data):
        """
        Initializes a new Regression object
        """
        self.data = data

    def linearAnalysis(self):
        """
        preforms a linear analysis on the data contained in Dataset object of the the regression object
        """
        # If there's no keys, there's no information needed for further process, thus error be thrown
        if self.data.keys() == []:
            raise ValueError("Dataset seems to be empty, cannot continue with linearAnalysis")
        xmin = self.data.getminkey()
        xmax = self.data.getmaxkey()
        fxmin = self.y(xmin)
        fxmax = self.y(xmax)
        return ([xmin, xmax], [fxmin, fxmax])

    def y(self, x):
        """
        Helper function for linearAnalysis, calculates the y value for a given x value
        """
        return self.a()*(x-self.xavg())+self.yavg()

    def xavg(self):
        """
        Helper function for linearAnalysis, determines the average value of the keys (x-values)
        """
        sum = 0
        for key in self.data.keys():
            sum += key
        return sum / len(self.data.keys())

    def yavg(self):
        """
        Helper function for linearAnalysis, determines the average value of the data (y-values)
        """
        sum = 0
        for key in self.data.keys():
            sum += self.data[key]
        return sum / len(self.data.keys())

    def SAK(self):
        """
        Helper function for linearAnalysis
        """
        sum = 0
        xavg = self.xavg()
        for key in self.data.keys():
            sum += (key - xavg) ** 2
        return sum

    def SAP(self):
        """
        Helper function for linearAnalysis
        """
        sum = 0
        xavg = self.xavg()
        for key in self.data.keys():
            sum += (key - xavg)*self.data[key]
        return sum

    def a(self):
        """
        Helper function for linearAnalysis
        """
        return self.SAP() / self.SAK()

    def plot(self):
        """
        Takes the Dataset object and plot it, then runs a linearAnalysis on the data and plots the result.
        Making a single plot with both raw data and the result of the linearAnalysis operation.
        """
        plt.figure()
        for key in self.data.keys():
            plt.plot(key, self.data[key], '*', color = 'red')
        x, y = self.linearAnalysis()
        plt.plot(x,y,color='green')
        plt.xlabel('L')
        plt.ylabel('T')
        plt.title('linearAnalysis Plot, and raw data')
        plt.xlim(x)
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # initialize a new Dataset Object
        a = Dataset()
        # import data from flueaeg.txt
        a.readDataPoints("flueaeg.txt")
        # initialize a new Regression Object
        reg = Regression(a)
        # Form a plot, with data from flueaeg.txt
        reg.plot()
        # We should now have a plot of a decreasing line with matching dots.

    # For debugging, run the program with any additional arguments, ei "python martin.haugaard.50.py foo"
    if len(sys.argv) > 1:
        """
        Dataset testing
        """
        print "a = Dataset()"
        a = Dataset()
        print "a[10] = 20"
        a[10] = 20
        print "a.get(10) == 20", a[10] == 20
        try:
            print "a.get(66)", a[66]
        except KeyError:
            print "As excepted there was a KeyError on keyvalue 66"
        print "a.__contains__(10)", a.__contains__(10)
        print "not a.__contains__(11)", not a.__contains__(11)
        print "New instance of Dataset, a = Dataset()"
        a = Dataset()
        print "readDataPoints form flueaeg.txt", a.readDataPoints("flueaeg.txt")
        print "len(a.keys()) == 10", len(a.keys()) == 10
        """
        Regression testing
        """
        print "reg = Regression(a)"
        reg = Regression(a)
        print "Average values of x (73) and y (19.99): ", reg.xavg(), reg.yavg()
        print "[xmin, xmax], [f(xmin) f(xmax)] :", reg.linearAnalysis()
        print "And a plot to show"
        reg.plot()