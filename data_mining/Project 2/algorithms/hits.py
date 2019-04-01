import timeit
import numpy as np
import math

EPSILON = 1e-10

def HubsAndAuthorities(A, nnodes):
    At = A.transpose()
    hubs = np.full(shape = (nnodes,1), fill_value = 1, dtype=np.float64)
    auths = np.full(shape = (nnodes,1), fill_value = 0, dtype=np.float64)


    while True:
        old_hubs = hubs
        old_auths = auths

        auths = np.dot(At, hubs)
        norm = 0
        for auth in auths:
            norm += math.pow(auth,2)
        norm = math.sqrt(norm)
        for auth in auths:
            auth /= norm

        norm = 0
        hubs = np.dot(A, auths) 
        for hub in hubs:
            norm += math.pow(hub, 2)
        norm = math.sqrt(norm)
        for hub in hubs:
            hub /= norm

        diff = 0
        for i in range(len(auths)):
            diff += math.fabs(old_auths[i] - auths[i])
        for i in range(len(hubs)):
            diff += math.fabs(old_hubs[i] - hubs[i])

        if diff < EPSILON:
            break


    return auths, hubs

def write(fname, auths, hubs, start, end):
    time = end - start

    fw = open('../hits_ans/' + fname + '_auths', 'w')
    for idx in range(0, len(auths)):
        fw.write(str(idx+1) + ' : ' + str(float(auths[idx])) + '\n')
    fw.write('Time ' + str(time) + '\n')
    fw.close()
    
    fw = open('../hits_ans/' + fname + '_hubs', 'w')
    for idx in range(0, len(hubs)):
        fw.write(str(idx+1) + ' : ' + str(float(hubs[idx])) + '\n')
    fw.write('Time ' + str(time) + '\n')
    fw.close()

def main():

    fnames = ['graph_1', 'graph_2', 'graph_3', 'graph_4', 'graph_5', 'graph_6', 'T10I4D100K_rule', 'T10I4D100K_trans', 'graph_1_increase_auth', 'graph_2_increase_auth', 'graph_3_increase_auth', 'graph_1_increase_hub', 'graph_2_increase_hub', 'graph_3_increase_hub']
    
    for fname in fnames:
        fr = open('../hw3dataset/' + fname + '.txt', 'r')
        raws = fr.readlines()
        fr.close()
        
        nnodes = -1
        nodes = set() 
        for raw in raws:
            src, des = raw.split('\n')[0].split('\r')[0].split(',')
            if int(src) > nnodes:
                nnodes = int(src)
            if int(des) > nnodes:
                nnodes = int(des) 
            nodes.add(int(src))
            nodes.add(int(des))

        A = np.full(shape = (nnodes,nnodes), fill_value = 0, dtype=np.float64)

        for raw in raws:
            src, des = raw.split('\n')[0].split('\r')[0].split(',')
            A[int(src)-1][int(des)-1] += 1

        start = timeit.default_timer()
        auths, hubs = HubsAndAuthorities(A, nnodes)
        end = timeit.default_timer()
        write(fname, auths, hubs, start, end)

        print fname + ' Finished'

        
if __name__ == '__main__':
    main()
