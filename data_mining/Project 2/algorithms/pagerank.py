import timeit
import numpy as np
from numpy.linalg import inv
import math

EPSILON = 1e-10

def PageRank(A, npages, d):
    M = np.full(shape = (npages,npages), fill_value = 0, dtype=np.float64)
    for ridx in range(0, npages):
        for cidx in range(0, npages):
            outlinks = np.sum(A[cidx])
            if A[cidx][ridx] > 0:
                M[ridx][cidx] = 1/outlinks
            else:
                M[ridx][cidx] = 0


    R = np.full(shape = (npages, 1), fill_value = 1, dtype=np.float64)

    while True:
        last_R = R
        R = np.dot(d, np.dot(M, R)) + np.dot(float((1-d))/npages, np.ones( (npages, 1)))

        diff = 0
        for page_idx in range(0, npages):
            diff += abs(R[page_idx] - last_R[page_idx])
        if diff <= EPSILON:
            return last_R



def write(fname, PageRank_value, start, end):
    time = end - start

    fw = open('../pagerank_ans_15/' + fname + '_pagerank', 'w')
    for idx in range(0, len(PageRank_value)):
        fw.write(str(idx+1) + ' : ' + str(float(PageRank_value[idx])) + '\n') 

    fw.write('Time: ' + str(time) + '\n')
    fw.close()

def main():

    d = 0.15

    fnames = ['graph_1', 'graph_2', 'graph_3', 'graph_4', 'graph_5', 'graph_6', 'T10I4D100K_rules', 'T10I4D100K_trans', 'graph_1_increase_pagerank', 'graph_2_increase_pagerank', 'graph_3_increase_pagerank']
    
    for fname in fnames:
        fr = open('../hw3dataset/' + fname + '.txt', 'r')
        raws = fr.readlines()
        fr.close()
        
        npages = -1
        nodes = set() 
        for raw in raws:
            src, des = raw.split('\n')[0].split('\r')[0].split(',')
            if int(src) > npages:
                npages = int(src)
            if int(des) > npages:
                npages = int(des) 
            nodes.add(int(src))
            nodes.add(int(des))

        A = np.full(shape = (npages,npages), fill_value = 0, dtype=np.float64)

        for raw in raws:
            src, des = raw.split('\n')[0].split('\r')[0].split(',')
            A[int(src)-1][int(des)-1] += 1

        start = timeit.default_timer()

        PageRank_value = PageRank(A, npages, d) 

        end = timeit.default_timer()

        write(fname, PageRank_value, start, end)

        print fname + ' Finished'

        
if __name__ == '__main__':
    main()
