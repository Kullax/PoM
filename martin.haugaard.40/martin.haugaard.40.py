# -*- coding: utf-8 -*-
from __future__ import division
__author__ = 'Martin Haugaard'


def compare_block_lengths(xrr):
    """
    Looks at an array of the array of arrays that is the input, and determines if they all share the same length
    if this is the case, True is returned, else False.
    :param xrr: An Array of Arrays
    :return: True if all elements in the Array of Arrays have the same length, else False.
    """
    l = len(xrr[0])
    for r in xrr:
        if len(r) != l:
            return False
    return True


def get_all_values(xrr):
    """
    :param xrr: Array of Array of elements
    :return: Each unique element in the Arrays inside the Array
    """
    # Sums all the sub-array into one single array
    s1 = sum(xrr, [])
    s2 = []
    # Makes a list s2 of unique elements, removing duplicates
    for i in s1:
        if i not in s2:
            s2.append(i)
    return s2


def compare_block_contents(xrr):
    """
    Will check the Array of Arrays to make sure that there's no double parings for any elements vs any other.
    Meaning each element in the Arrays will only occur at most once with each other element.
    :param xrr: An Array of Arrays containing elements
    :return: True if no element occurs alongside another more than once, False if not
    """
    # Get a complete list of contenders in the block structure
    contenders = get_all_values(xrr)
    # We now check for each contender, if they'll be unfairly matched
    for i in contenders:
        # From all the contenders, I'm currently interested in the opponents of the current contender 'i'
        opponents = contenders[:]
        opponents.remove(i)
        for rr in xrr:
            # I'm only interested in the Arrays which contain the 'i' I'm looking at
            if rr.__contains__(i):
                for r in rr:
                    # I'm interested in each of the opponents in the current block
                    if r != i:
                        # If the opponent is still within the contender list, we haven't met this contender before,
                        if contenders.__contains__(r):
                        # but now we have, so it's removed from the contender list
                            contenders.remove(r)
                        else:
                            # There's a contender, which we've already met, so the block is not balanced.
                            return False
    # There was no duplicate matches, so True is returned
    return True


def is_BS(xrr):
    """
    Will check if the input, xrr, is a valid block structure, meaning that each Array in the Array of Arrays,
    all have the same length, while also making sure that no element withing the Arrays appears alongside another
    element more than once
    :param xrr: An Array of Arrays of elements
    :return: True if the Array of Arrays matches that of a Block Structure, False if not
    """
    return compare_block_lengths(xrr) and compare_block_contents(xrr)


if __name__ == "__main__":
    # Given the blocks in the assignment, I will check if my function works for B2, B3 and B5, of which B2 and B5 should
    # be true, while B3 should be false
    B2 = [['A', 'B', 'C'], ['A', 'D', 'G'], ['A', 'E', 'F'], ['B', 'D', 'F'], ['B', 'E', 'G'], ['C', 'D', 'E'],
          ['C', 'F', 'G']]
    print "Is B2 a block structure?", is_BS(B2)
    B3 = [['a', 'b'], ['a', 'c', 'f'], ['a', 'd', 'e'], ['b', 'c', 'e'], ['b', 'd', 'f'], ['c', 'd'], ['e', 'f']]
    print "Is B3 a block structure?", is_BS(B3)
    B5 = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [1, 5, 6], [2, 3, 7], [0, 5, 7],
          [1, 3, 8], [2, 4, 6]]
    print "Is B5 a block structure?", is_BS(B5)