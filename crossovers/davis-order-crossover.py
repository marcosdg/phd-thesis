# -*- coding: utf-8 -*-
# davis-crossover.py
# Author: Marcos Diez García
# 26 Oct 2018


from itertools import groupby

## AUXILIARY FUNCTIONS

# remove_duplicates(ls):
#   Input: ls
#   Output: ls without duplicate elements
#
#   Note: remove_duplicates works also there are nested lists within ls.
def remove_duplicates(ls):
    # groupby needs ls to be sorted first
    new = sorted(ls)
    return list(key for key,val in groupby(new))

# ls1_setminus_ls2(ls1, ls2):
#   Input:  ls1, the list we want to remove elements from.
#   Input:  ls2, with the elements we want to remove in ls1.
#   Output: ls1 setminus ls2: all elements in ls1 not appearing in ls2.
#
#   Examples:
#       ls1 = [1,2,3,4], ls2 = [2,3], out = [1,4]
#       ls1 = [2,3,9], ls1 = [1,2,2,4,3], out = [9]
#
#   Note: removing duplicates in ls2 beforehand is harmless to the end
#   result, because all we care in ls2 is which elements appear, not their
#   order or number of occurrences.
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


# all_davis_xover(x, y):
#   Input: parent x
#   Input: parent y
#   Output: all possible different offspring obtained using davis order
#           crossover on parent x and y, for all possible crossover sections.
def all_davis_xover(x, y):
    oll = []
    length = len(x)

    for i in range(0, length):
        for j in range(i, length):
            z1 = davis_xover(x, y, i, j)
            z2 = davis_xover(y, x, i, j)
            oll.append(z1)
            oll.append(z2)

    return remove_duplicates(oll)

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

    all1 = all_davis_xover(x1, y1)
    #all2 = all_davis_xover(x2, y2)
    #all3 = all_davis_xover(x3, y3)
    #all4 = all_davis_xover(x4, y4)

    print("Parent x: " + str(x1))
    print("Parent y: " + str(y1))
    print("# Different offspring: " + str(len(all1)))
    print("Offspring:")
    print(all1)


if __name__ == "__main__":
    main()


