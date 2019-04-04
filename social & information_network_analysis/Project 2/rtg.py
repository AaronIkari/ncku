import numpy as np
import matplotlib
matplotlib.use('Agg')
import itertools as it
import sys
import networkx as nx
import matplotlib.pyplot as plt
import time
import community

NUM_CHARACTERS = 26
NODE_SIZE = 10
ALPHA = 0.4

def rtg(num_edges, num_chars, beta, q):

    if num_chars > NUM_CHARACTERS or num_chars < 0:
        raise Error('Number of characters cannot be greater than 26 or less than 0')
    if num_edges < 0:
        raise Error('Number of edges cannot less than 0')
    if beta > 1 or beta < 0:
        raise Error('0 <= beta <= 1')
    if q > 1 or q < 0:
        raise Error('0 <= q <= 1')


    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 
                 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    # '#' terminated
    characters = characters[:num_chars] + ['#']

    # initialize keyboard
    keyboard = gen_keyboard(num_chars, q, beta)
    edges = []
    for _ in range(num_edges):
        edges.append(create_edge(characters, keyboard))
    return edges


def gen_keyboard(num_chars, q, beta):
    # assign unequal probabilities to the keys
    p = np.zeros(num_chars + 1)
    p_remaining = 1 - q
    for i in range(num_chars - 1):
        p[i] = np.random.rand() * p_remaining
        p_remaining -= p[i]
    p[num_chars - 1] = p_remaining
    # last key is the seperator
    p[num_chars] = q

    # init the keyboard with indipendant cross product probs 
    keyboard = np.outer(p, p)
    # multiply the imbalance factor
    keyboard = keyboard * beta
    # set diagonal to 0
    np.fill_diagonal(keyboard, 0) 
    # calculate remaining probabilities for the diagonal
    # such that each row and column sums up to the 
    # marginal probability
    remaining_diag = p - keyboard.sum(axis=0)
    dia_idx = np.diag_indices_from(keyboard)
    keyboard[dia_idx] = remaining_diag

    return keyboard

    
def create_edge(characters, keyboard):
    src_terminated = False
    dst_terminated = False
    src = ''
    dst = ''
    char_combi = np.fromiter(it.product(characters, characters), 
                                dtype='1str,1str')

    while not (src_terminated and dst_terminated):
        s, d = np.random.choice(char_combi, p=keyboard.flatten())
        if not src_terminated:
            src += s
        if not dst_terminated:
            dst += d
        if s == '#':
            src_terminated = True
        if d == '#':
            dst_terminated = True

        
    # recursive call
    if (src == dst):
        return create_edge(characters, keyboard)
    else:
        return (src, dst)

def plot_degree_distribution(G):
    degrees = [val for (node, val) in G.degree()]
    counts, bins, patches = plt.hist(degrees, bins=100)

    # degree distribution - power law
	# create figure
    fig, ax = plt.subplots()
	# plot bar
    ax.bar(bins[:-1], counts/float(sum(counts)), width=bins[1]-bins[0])
	# plot set x/y-label and title
    ax.set(xlabel='Degree', ylabel='Fraction of nodes', title='Degree Distribution')
	# plot enable gird
    ax.grid()
	# save figure
    fig.savefig('degree distribution (power law)')


def plot_log_log_scatter_degree_distribution(G):
    degrees = [val for (node, val) in G.degree()]
    counts, bins, patches = plt.hist(degrees, bins=100)

    counts_nozero = counts*1.
    counts_nozero[counts==0] = -float('Inf')

	# create figure
    fig, ax = plt.subplots()
	# plot log-log scatter
    ax.scatter(bins[:-1], counts_nozero/float(sum(counts)), s=60)
	# plot set x/y-label and title
    ax.set(xlabel='Degree', ylabel='Fractions of nodes', title='Log-Log Scatter Degree Distribution', xscale='log', yscale='log')
	# plot enable gird
    ax.grid()
	# save figure
    fig.savefig('log-log scatter degree distribution (power law)')

def plot_graph(G):

    fig, ax = plt.subplots(figsize=(20,20))
    ax.set(xlabel='x', ylabel='y', title='Graph Visualization')
    # node position
    pos=nx.spring_layout(G)
    # network nodes
    nx.draw_networkx_nodes(G, pos, node_size=NODE_SIZE)
    # network edges
    nx.draw_networkx_edges(G, pos, alpha=ALPHA)

    # save figure
    fig.savefig('Graph.png')

def plot_time_diff_w(time_list):
    fig, ax = plt.subplots()
    ax.plot(np.arange(0.2, 2.1, 0.1), time_list, 'b-o')
    ax.set(xlabel='w', ylabel='Time(sec)')
    fig.savefig('Time.png')

def main():
   
    time_list = list()
    W = [0.2e6, 0.3e6, 0.4e6, 0.5e6, 0.6e6, 0.7e6, 0.8e6, 0.9e6, 1.0e6, 1.1e6, 1.2e6, 1.3e6, 1.4e6, 1.5e6, 1.6e6, 1.7e6, 1.8e6, 1.9e6, 2.0e6]
    for w in W:
        start = time.time()
        pairs = rtg(int(w), 2, 0.95, 0.8)
        end = time.time()
        time_list.append(end-start)
        nodes = set()
        edges = list()
        for pair in pairs:
            nodes.add(pair[0])
            nodes.add(pair[1])
            edges.append( (pair[0], pair[1]) )

        # graph
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        GCC = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)

        if w == 0.6e6:
          plot_degree_distribution(G)
          plot_log_log_scatter_degree_distribution(G)
          plot_graph(G)
          print 'cluster coefficient %f' %nx.average_clustering(G)
          print 'average path length on largest connected component: %f' %nx.average_shortest_path_length(GCC[0])

    plot_time_diff_w(time_list) 
          
          
if __name__ == '__main__':
    main()
