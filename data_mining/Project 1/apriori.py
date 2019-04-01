import timeit
import sys
from collections import defaultdict

''' read file '''
def readFile(fn):
    # transaction record
    T = list()
    # initial candidate itemset
    C1 = set()

    with open(fn, 'r') as fn:
        for ln in fn:
            lnSet = set(ln.strip('\n').split(','))
            C1 = C1.union(lnSet)
            T.append(lnSet)

    return T, C1

''' generate next frequent itemset '''
def genNextL(T, C, minSup, supCnt, pruneSet):
    # frequent itemset
    L = set()

    # scan D for count of each candodate
    for item in C:
        for transac in T:
            if transac.issuperset(item):
                supCnt[item] += 1
    # compare candidate suppor count with minimum support count
    for item in C:
        # less than minimum support count
        if supCnt[item] < minSup :
            pruneSet.add(item)
        else:
            L.add(item)

    return L, supCnt, pruneSet

''' genrate next candidate '''
def genNextC(L, pruneSet):
    # candidate itemset
    C = set()
    # turn set(non-indexing) to list for indexing purpose
    L = list(L)

    for idx in range(0, len(L)):
        for idxx in range(idx + 1, len(L)):
            # first set
            f = set(L[idx])
            # second set
            s = set(L[idxx])

            if len(f.intersection(s)) != len(L[idx]) - 1:
                continue

            mergeSet = set()
            mergeSet.update(L[idx])
            mergeSet.update(L[idxx])

            # keep inner set complete
            innerSet = frozenset(mergeSet)

            # prune or not 
            ifPrune = False
            for seed in pruneSet:
                if innerSet.issuperset(seed):
                    ifPrune = True

            if not ifPrune:
                C.add(innerSet)
            else:
                pruneSet.add(innerSet)

    return C, pruneSet

''' run Apriori algorithm '''
def runApriori(T, C1, minSup):
    # All frequent itemset 
    feqItemset = list()

    # prune set: set
    pruneSet = set()

    # support count: dictionary 
    supCnt = defaultdict(int)

    # initial candidate itemset
    C = C1

    # get one-frequent itemset
    L, supCnt, pruneSet = genNextL(T, C, minSup, supCnt, pruneSet)
    feqItemset.append(L)

    supCnt.clear()
    pruneSet.clear()

    while(True):
        # generate Ck+1 candidates from Lk
        C, pruneSet = genNextC(L, pruneSet)

        # find frequent itemset (Lk) from Ck
        L, supCnt, pruneSet = genNextL(T, C, minSup, supCnt, pruneSet)
        feqItemset.append(L)
        
        if len(L) is 0:
            break

        supCnt.clear()
        pruneSet.clear()
    
    return feqItemset

''' main function '''
def main():

    # file name
    fn = sys.argv[1]
    # minimum support
    minSup = int(sys.argv[2])

    # read file
    # get transaction reocrd and initial candidate itemset
    T, C1 = readFile(fn)

    start = timeit.default_timer()

    # run apriori
    feqItemset = runApriori(T, C1, minSup)

    end = timeit.default_timer()

    for it in range(0, len(feqItemset)):
        print " - -", it, "th iteration - -"
        print feqItemset[it]

    print "\nTime taken: ", end - start, "seconds."


if __name__ == '__main__':
    main()
