import timeit
import numpy as np
import math

ITERATION = 5

def SimRank(in_neighbors, nnodes, C = 0.8):
    S_k = np.identity(nnodes)
    S_nk = np.zeros([nnodes, nnodes])

    for t in range(ITERATION):

        for i in range(nnodes):
            for j in range(nnodes):
                if i == j:
                    S_nk[i][j] = 1

                else:
                    i_in_neighbor = len(in_neighbors[i+1])
                    j_in_neighbor = len(in_neighbors[j+1])
                    if i_in_neighbor == 0 or j_in_neighbor == 0:
                        S_nk[i][j] = 0
                    else:
                        prefix = C/(i_in_neighbor * j_in_neighbor)
                        postfix = 0
                        for ii in in_neighbors[i+1]:
                            for ij in in_neighbors[j+1]:
                                postfix += S_k[int(ii)-1][int(ij)-1] 
                        S_nk[i][j] = prefix * postfix

        S_k = S_nk.copy()
        S_nk.fill(0)


    return S_k


        

def write(fname, S, start, end, nnodes):
    time = end - start

    fw = open('../simrank_ans/' + fname + '_simrank', 'w')
    for i in range(nnodes):
        for j in range(nnodes):
            if i <= j:
                fw.write('(%s, %s): %s\n' %(str(i), str(j), S[i][j])) 
    fw.write('Time: ' + str(time) + '\n')
    fw.close()

def main():

    fnames = ['graph_1', 'graph_2', 'graph_3', 'graph_4', 'graph_5']
    #fnames = ['graph_3']
     
    for fname in fnames:
        fr = open('../hw3dataset/' + fname + '.txt', 'r')
        raws = fr.readlines()
        fr.close()
        
        nnodes = -1
        for raw in raws:
            src, des = raw.split('\n')[0].split('\r')[0].split(',')
            if int(src) > nnodes:
                nnodes = int(src)
            if int(des) > nnodes:
                nnodes = int(des) 

        in_neighbors = dict()
        for i in range(1, nnodes+1):
            in_neighbors[i] = set()

        for raw in raws:
            src, des = raw.split('\n')[0].split('\r')[0].split(',')
            in_neighbors[int(des)].add(src)

        start = timeit.default_timer()

        S = SimRank(in_neighbors, nnodes, 0.8)

        end = timeit.default_timer()

        write(fname, S, start, end, nnodes)

        print fname + ' Finished'

        
if __name__ == '__main__':
    main()
