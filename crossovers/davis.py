# -*- coding: utf-8 -*-
# davis-crossover.py
# Author: Marcos Diez García
# 26 Oct 2018


import itertools

## AUXILIARY FUNCTIONS

# remove_duplicates(ls):
#   Input:  list ls
#   Output: ls without duplicate elements
#
#   Note: remove_duplicates also works if ls is a list of lists.
def remove_duplicates(ls):
    # groupby needs ls to be sorted first
    new = sorted(ls)
    return list(key for key,val in itertools.groupby(new))

# flatten(ls):
#   Input:  list ls
#   Output: flattens all nested lists of ls
#
#   Example:
#       ls1             =  [[1,2], [2,3]]
#       ls2             =  [[1,2,3], [1,2,3], [[1,2,3],[3,2,1]]]
#       flatten(ls1)    =  [1,2,2,3]
#       flatten(ls2)    =  [1, 2, 3, 1, 2, 3, [1, 2, 3], [3, 2, 1]]
#       
def flatten(ls):
    return list(itertools.chain.from_iterable(ls))

# ls1_setminus_ls2(ls1, ls2):
#   Input:  ls1, the list we want to remove elements from.
#   Input:  ls2, the list with elements we want to remove in ls1.
#   Output: ls1 setminus ls2,  all elements in ls1 not appearing in ls2.
#
#   Examples:
#       ls1 = [1,2,3,4], ls2 = [2,3],       out = [1,4]
#       ls1 = [2,3,9],   ls2 = [1,2,2,4,3], out = [9]
#
#   Note: ls1 and ls2 MUST NOT contain nested lists
#   Note: removing duplicates in ls2 beforehand is harmless to the end result.
#   All we care in ls2 is which elements appear, not their order or number of
#   occurrences.
def ls1_setminus_ls2(ls1, ls2):
    ls2_set = set(ls2)
    return [item for item in ls1 if item not in ls2]

## DAVIS ORDER CROSSOVER
#
# davis_xover(x, y, i, j):
#   Input: x, the 1st  parent used as the ‘cutter’ string.
#   Input: y, the 2nd parent used as the ‘filler’ string.
#   Input: i, the index for the start of crossover section.
#   Input: j, the index for the end of crossover section.
#   Output: the offspring z of x and y that preserves relative order of
#           symbols of the parents.
#
#   Notes:
#   * x and y are lists of the same length.
#   * 1 <= i < j <= n. Or equivalently, i ∈  [1, j) , j ∈  [i + 1, n + 1)
#   * Main algorithm steps:
#       1.  Get from y those elements, the fillers, not appearing in the
#            xover section. Consider this list as a queue onwards.
#       2.  For each index in 1..n do:
#       2.1.    If index belongs to xover section then:
#       2.1.1.      z[index] = x[index] # copy xover sect. verbatim
#       2.2     Else: # outsise xover section
#       2.2.1.      z[index] = remaining[0] # copy next unused filler
#       2.2.2.      remaining.pop(0)        # remove the filler just used
#
def davis_xover(x, y, i, j):
    # Init
    z = []
    length = len(x)
    xover_sect = x[i:j+1] # [i, j + 1) = [i, j]
    # Main
    fillers = ls1_setminus_ls2(y, xover_sect)
    for at in range(length):
        # copy xover section
        if i <= at <= j:
            z.insert(at, x[at])
        # use fillers
        else:
            filler = fillers.pop(0) # pop returns 1st elem and deletes it.
            z.insert(at, filler)
    return z

# davis_xover_support(x, y):
#   Input: x, the 1st  parent used as the ‘cutter’ string.
#   Input: y, the 2nd parent used as the ‘filler’ string.
#   Output: all possible different offspring obtained using davis order
#           crossover on parents x and y, for all possible crossover sections.
def davis_xover_support(x,y):
    oll = []
    length = len(x)

    for i in range(0, length):
        for j in range(i, length):
            z = davis_xover(x,y,i,j)
            oll.append(z)
    return remove_duplicates(oll)

## SYMMETRIC DAVIS ORDER CROSSOVER
#
# symmetric_davis_xover_support(x, y):
#   Input: parent x
#   Input: parent y
#   Output: all possible different offspring obtained using davis order
#           crossover on parent pairs (x,y) and (y,x), for all possible
#           crossover sections.
def symmetric_davis_xover_support(x, y):
    oll = []
    length = len(x)

    for i in range(0, length):
        for j in range(i, length):
            z1 = davis_xover(x, y, i, j)
            z2 = davis_xover(y, x, i, j)
            oll.append(z1)
            oll.append(z2)
    return remove_duplicates(oll)

## RECURSIVE CLOSURE FOR (DAVIS ORDER) CROSSOVERS
#
# closure(xover,sett,k):
#   Input: xover, a binary crossover function. For instance, davis_xover_support
#          or its symmetric_davis_xover_support.
#   Input: sett, a set of individuals (permutations)
#   Input: k, a natural number (number of recursive calls)
#   Output: all possible descendants that can be obtained by applying xover
#           crossover to the input set sett, and then again to the offspring
#           set, and again to the grandchildren, for as many times as k.
def closure(xover,sett,k):
    closed = []
    offs = []

    if k == 0:
        closed = sett
    else:
        for x in sett:
            for y in sett:
                offs.append(xover(x,y))
        offs = remove_duplicates(flatten(offs))
        closed = closure(xover, offs, k-1)
    return closed

## MAIN
def main():
    # Some pairs of parents to try
    x1 = [1,2,3]
    y1 = [3,1,2]
    #x2 = [1,2,3,4]
    #y2 = [2,3,4,3]
    #x3 = ['A','B','C','D']
    #y3 = ['B','A','D','C']
    #x4 = ['A','B','C','D','E','F','G']
    #y4 = ['D','B','A','C','G','F','E']

    all1 = symmetric_davis_xover_support(x1, y1)
    #all2 = davis_xover_support(x1, y1)
    #closure_davis_1 = closure(davis_xover_support, [x1,y1], 1)
    #closure_davis_2 = closure(davis_xover_support, [x1,y1],2)
    #closure_symdavis_1 = closure(symmetric_davis_xover_support, [x1,y1],1)
    #closure_symdavis_2 = closure(symmetric_davis_xover_support, [x1,y1],2)

    print("Parent x: " + str(x1))
    print("Parent y: " + str(y1))
    print("# Different offspring: " + str(len(all1)))
    print("Offspring:")
    print(all1)


if __name__ == "__main__":
    main()


