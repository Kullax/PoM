#-*- coding: UTF-8 -*-
__author__ = 'Martin Simon Haugaard'
"""
A simple implementation of a matrix, using only the build in python functions
"""


class simplematrix():
    m = None
    n = None
    values = None

    def __init__(self, m=0, n=0, values=[]):
        """
        Initializes the simplematrix object, takes tree arguments, two describing the dimensions, and a third a list
        with the content of the matrix, read from left to right, top to buttom.
        If fewer values are given than the dimensions can hold, remaining values are set to zero.
        If more are given, any additional values will be skipped.
        :param m: first dimension
        :param n: second dimension
        :param values: a list of values for the matrix,
        """
        self.m = m
        self.n = n
        self.values = [[0 for _ in xrange(m)] for _ in xrange(n)]
        value = 0
        for i in xrange(self.n):
            for j in xrange(self.m):
                if value >= len(values):
                    break
                (self.values[i])[j] = values[value]
                value += 1

    def __str__(self):
        """
        Prints the simplematrix object, by creating a string describing the content of the object
        :return: a string with information on the object
        """
        output = ""
        for i in self.values:
            st = []
            output += "["
            for j in i:
                st.append(str(j))
            output += ",".join(st)+"]"
        return str(self.m)+"x"+str(self.n)+" [" + output + "]"

    def __add__(self, other):
        """
        Preforms a simple addition on two simplematrix objects, when two simplematrix objects are connected by a '+'
        operator.
        :return: a simplematrix object with the results of the addition.
        """
        if (self.m != other.m) or (self.n != other.n):
            raise TypeError("Dimensions of matrices does not match")
        tmp = [[0 for _ in xrange(self.m)] for _ in xrange(self.n)]
        for i in xrange(self.n):
            for j in xrange(self.m):
                tmp[i][j] = self.values[i][j] + other.values[i][j]
        res = []
        for i in tmp:
            res += i
        return simplematrix(self.m, self.n, res)

    def __mul__(self, other):
        """
        Preforms a matrix multiplication on two simplematrix objects when two simplematrix objects are connected by a
        '*' operator.
        :return: a simplematrix object with the results of the mutiplication
        """
        if self.n != other.m:
            raise TypeError("Illegal dimensions for mul operator")
        tmp = [[0 for _ in xrange(self.n)] for _ in xrange(other.m)]
        for i in xrange(self.n):
            for j in xrange(other.m):
                for k in xrange(other.n):
                    tmp[i][j] += self.values[i][k] * other.values[k][j]
        res = []
        for i in tmp:
            res += i
        return simplematrix(self.n, other.m, res)

    def __eq__(self, other):
        """
        Will check if the values of two simplematrix objects, of equal dimensions, are equal (==).
        :return: True, iff the values are equal in both objects
        """
        if self.n != other.n or self.m != other.m:
            raise TypeError("Illegal dimensions for eq operator (%s x %s - %s x %s)" %
                            (self.n, self.m, other.n, other.m))
        return self.values == other.values

    def __ne__(self, other):
        """
        Will check if the values of two simplematrix objects, of equal dimensions, are not equal (!=).
        They are not equal iff the values of the simplematrix objects doesn't match.
        :return: False, iff the values of the objects differ
        """
        if self.n != other.n or self.m != other.m:
            raise TypeError("Illegal dimensions for ne operator (%s x %s - %s x %s)" %
                            (self.n, self.m, other.n, other.m))
        return not(self.values == other.values)

    def read(self, filename):
        """
        Overwrites the current simplematrix by reading information stored in a file.
        Reads a file for a simplematrix, first two lines should be dimensions, and any additional lines should be
        values of the simplematrix.
        Once the filename is read, a new initialization of the simplematrix is made, with the read data.
        :param filename: location of simplematrix
        """
        f = open(filename, 'r')
        m = f.readline()
        n = f.readline()
        lst = []
        for line in f.readlines():
            lst.append(int(line))
        f.closed
        self.__init__(int(m), int(n), lst)

    def write(self, filename):
        """
        Saves the current simplematrix layout to a filelocation, as a series of lines.
        first two lines are the dimensions of the matrix, any lines beyond this are the values of the matrix
        :param filename: a file location, will make file if not present
        """
        f = open(filename, 'w')
        f.write(str(self.m) + "\n")
        f.write(str(self.n) + "\n")
        for i in self.values:
            for j in i:
                f.write(str(j)+"\n")
        f.closed


if __name__ == "__main__":
    """
    First I initialize a few test matrix
    """
    print "Initializing a few different matrix of different sizes"
    s0 = simplematrix()
    print "Simplematrix with no value or dimension given:\n", s0
    s1 = simplematrix(1, 2)
    print "Simplematrix with dimensions 1x2 but no values:\n", s1
    s2 = simplematrix(4, 2, [1, 2, 3, 4, 5, 6, 7, 8])
    print "Simplematrix with dimensions 4x2 and arguments [1, 2, 3, 4, 5, 6, 7, 8]\n", s2

    """
    Now to preform a few operations on the matrix
    """
    print "Test of matrix addition"
    A = simplematrix(2, 2, [1, 2, 3, 4])
    print "A: ", A
    B = simplematrix(2, 2, [5, 6, 7, 8])
    print "B: ", B
    C = simplematrix(2, 2, [6, 8, 10, 12])
    print "C: ", C
    print "C == A + B: ", C == A + B
    print "Now randomly generated matrix"
    import random
    A = simplematrix(3, 2, random.sample(xrange(10), 6))
    B = simplematrix(3, 2, random.sample(xrange(10), 6))
    C = A + B
    print str(A) + " + " + str(B) + " = " + str(C), C == A + B
    print "Reading matrix from A.matrix and B.matrix"
    print A.read("A.matrix"), A == simplematrix(4, 2, [1, 2, 3, 4, 5, 6, 7, 8])
    print B.read("B.matrix"), B == simplematrix(4, 2, [11, 3, 6, 0, 3, 2, 0, 1])
    print "Writing to C.matrix"
    C.write("C.matrix")
    print "Testing simple associations"
    print "A == A: ", A == A
    print "B != A: ", B != A
    print "Finally, Multiplication Test:"
    A.read("A2.matrix")
    B.read("B2.matrix")
    print "A: ", A, A == simplematrix(3, 2, [1, 2, 3, 5, 6, 7])
    print "B: ", B, B == simplematrix(2, 3, [5, 3, 0, 1, 4, 2])
    print "A*B: ", A*B, A*B == simplematrix(2, 2, [17, 11, 53, 35])
