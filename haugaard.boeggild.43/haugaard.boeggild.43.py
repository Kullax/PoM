# -*- coding: utf-8 -*-
from __future__ import division
from math import e
from pylab import *

plt_number = 0


def cosx(x):
    """
    Simple placeholder function for calculating cos of x
    :param x: integer value for calculating cos(x)
    :return: result of cos(x)
    """
    return math.cos(x)


def sqrtexp(x):
    """
    Placeholder function for calculating the second given funciton
    :param x: the current value to be processed
    :return: the result given the supplied x
    """
    return 1/math.sqrt(2*math.pi)*e**(-x**2/2)


def sinx(x):
    """
    Placeholder function for calculating sin(1/x)
    :param x: integer value for calculating sin(1/x)
    :return: result of sin(1/x)
    """
    return math.sin(1/x)


def getStepLength(a, b, n):
    """
    Given a length from a to b, will return the step size needed to achieve n steps.
    :param a: the start value
    :param b: the end value
    :param n: the number of steps requested
    :return: the length of the steps, needed to achieve n steps form a to b
    """
    return (b-a) / n


def rInt(f, a, b, n):
    """
    Calculates the Riemann sum of a function given an interval between a and b.
    Calculations are made from a selection of n calculations evenly distributed along the interval
    :param f: Function in question
    :param a: start value of the interval for the function
    :param b: end value of the interval for the function
    :param n: the number of calculations made in order to calculate the Riemann sum
    :return: Integration sum calculated using the Riemann sum method
    """
    s = 0
    i = a
    step = getStepLength(a, b, n)
    while i <= b:
        s += f(i)*step
        i += step
    return s


def rIntMid(f, a, b, n):
    """
    Calculates the Riemann sum of a function given an interval between a and b.
    Calculations are made from a selection of n calculations evenly distributed along the interval
    Unlike rInt, calculations are now used observing mass of triangles, instead of the mass of rectangles.
    This should supply a more accurate result, but may vary.
    :param f: Function in question
    :param a: start value of the interval for the function
    :param b: end value of the interval for the function
    :param n: the number of calculations made in order to calculate the Riemann sum
    :return: Integration sum calculated using the Riemann sum method
    """
    s = 0
    step = getStepLength(a, b, n)
    i = a+step
    while i <= b:
        s += step * 0.5 *(f(i)+f(i-step))
        i += step
    return s


def plotfigure(f, a, b, n):
    """
    A helper function, for creating two plots, showcasing the Riemann sums, using different numbers of steps.
    Two plots are presented, top using rInt and bottom using rIntMid.
    :param f: the function to plot sums for
    :param a: the start of the interval for the function
    :param b: the end of the interval for the function
    :param n: the number of total steps tested.
    :return: None - a plot is presented.
    """
    global plt_number
    plt.figure(plt_number)
    plt.subplot(211)
    n = range(1, n, 1)
    q = []
    for i in n:
        q.append(rInt(f, a, b, i))
    plt.plot(n, q, 'ro')
    plt.subplot(212)
    q = []
    for i in n:
        q.append(rIntMid(f, a, b, i))
    plt.plot(n, q, 'o')
    plt.show()
    plt_number += 1


if __name__ == "__main__":
    a = 0
    b = 2*math.pi
    n = 1000
    print "rInt sum, over interval [%d,%f], in cosx, using n=%d:" % (a, b, n)
    print rInt(cosx, a, b, n)
    print "rIntMid sum, over interval [%d,%f], in cosx, using n=%d:" % (a, b, n)
    print rIntMid(cosx, a, b, n)
    # Forventer værdi tæt på nul
    a = -10
    b = 10
    n = 100
    print "rInt sum, over interval [%d,%f], in sqrtexp, using n=%d:" % (a, b, n)
    print rInt(sqrtexp, a, b, n)
    print "rIntMid sum, over interval [%d,%f], in sqrtexp, using n=%d:" % (a, b, n)
    print rIntMid(sqrtexp, a, b, n)
    # Forventer værdi tæt på 1
    a = 0.001
    b = 10
    n = 400
    print "rInt sum, over interval [%d,%f], in sinx, using n=%d:" % (a, b, n)
    print rInt(sinx, a, b, n)
    print "rIntMid sum, over interval [%d,%f], in sinx, using n=%d:" % (a, b, n)
    print rIntMid(sinx, a, b, n)
    # Forventer værdi tæt på 2.7262
    plotfigure(cosx, 0, 2*math.pi, 250)
    plotfigure(sqrtexp, -10, 10, 100)
    plotfigure(sinx, 0.001, 10,100)
#    plotfigure(sinx, 0.001, 10,10000)