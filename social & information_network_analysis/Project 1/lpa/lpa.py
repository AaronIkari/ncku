import networkx as nx
from collections import Counter
import random

def read():
    nodes = set()
    edges = list()

    with open('networkdata.txt') as fr:
        rows = fr.readlines()
        for row in rows:
            row = row.strip('\n').split('\t')

            nodes.add(row[0])
            nodes.add(row[1])
            edges.append( (row[0], row[1]) )

    nodes = list(nodes)

    return nodes, edges

def write(G):
    with open('output.txt', 'w') as fw:
        for node in G.nodes:
            fw.write('%s\t%s\n' %(node, G.node[node]['cur_label']) )


def main():
    nodes, edges = read()

    # create empty graph
    G = nx.Graph()

    # add nodes to G
    for node in nodes:
        G.add_node(node, pre_label = node, cur_label = None)

    # add edges to G
    G.add_edges_from(edges)
   
    ITERATION = 6
    while(ITERATION > 0):

        for node in G.nodes:
            neighbor_label = list() 
            majority = list()
            maxv = -1
            for neighbor in G.neighbors(node):
                neighbor_label.append(G.node[neighbor]['pre_label'])
            counter = Counter(neighbor_label)
            for value, count in counter.most_common():
                if count >= maxv:
                    maxv = count
                    majority.append(value)
            print majority
            G.node[node]['cur_label'] = random.choice(majority)

        ITERATION -= 1


    write(G)

if __name__ == '__main__':
    main()
