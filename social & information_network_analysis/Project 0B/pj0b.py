import networkx as nx
from priorityQueue import PriorityQueue as PQ

MAXINT = 2147483647

''' read file from movie_nodes.txt and movie_edgesw.txt '''
def read(G):

    # id to name & name to id dictionary
    id_to_name = dict()
    name_to_id = dict()
    # distance dictionary
    distance = dict()
    # predecessor dictionary
    predecessor = dict()
    # priority queue
    pq = PQ()

    # read nodes from movie_nodes.txt
    with open('movie_nodes.txt') as fn:
        # read data rows from file
        rows = fn.readlines()
        # for each row
        for row in rows:
            # string token
            tokens = row.strip('\n').split('\t')
            # dictionary for id -> name
            id_to_name[ tokens[0] ] = tokens[1]
            # dictionary for name -> id
            name_to_id[ tokens[1] ] = tokens[0]
            # graph add node
            G.add_node( tokens[0] )
            # initialize all nodes distance
            distance[ tokens[0] ] = MAXINT 
            # initialize priority queue
            pq.add_task(tokens[0], MAXINT)
            # initialize all nodes predecessor
            predecessor[ tokens[0] ] = None
        # close file
        fn.close()

    # read edges from movie_edgesw.txt
    with open('movie_edgesw.txt') as fn:
        # read data rows from file
        rows = fn.readlines()
        # for each row
        for row in rows:
            # string token
            tokens = row.strip('\n').split('\t')
            # graph add edges
            G.add_edge(tokens[0], tokens[1], weight = float(tokens[2]))
        # close file
        fn.close()


    return id_to_name, name_to_id, distance, predecessor, pq, G


''' main function '''
def main():
    # empty graph
    G = nx.Graph()

    # read nodes/edges from movie_nodes.txt and movie_edgesw.txt
    id_to_name, name_to_id, distance, predecessor, pq, G = read(G)

    # source(src) node
    src = 'Angelina Jolie'
    # target(tar) node
    tar = 'Megan Fox'

    # setup initial distance for source(src) node equal to 0
    distance[ name_to_id[src] ] = 0
    # update source(src) node to priority queue
    pq.add_task( name_to_id[src], 0)

    # debug variable
    total = pq.size()

    # until priority queue empty
    while pq.size() != 0:

        # debug message - begin
        print("{0} left".format(pq.size()))
        # debug message - end

        # pop from priority queue
        node, priority = pq.pop_item()

        # debug message - begin
        print("{0} pop up".format(node))
        print("progress {0}%".format((total - pq.size())/total*100) )
        print("---------------------------\n")
        # debug message - end

        # stop point
        if distance[node] == MAXINT:
            break

        # current node distance
        currentDistance = distance[node]

        # visit current node's neigbors
        for neighbor in G.neighbors(node):
            # new distance = current node distance + w(current node, neighbor)
            newDistance = currentDistance + G[node][ neighbor ]['weight']
           
            # update distance for current node
            # label current node predecessor
            # update priority queue 
            if newDistance < distance[neighbor]:
                distance[neighbor] = newDistance
                predecessor[neighbor] = node
                pq.add_task(neighbor, newDistance)

    # record path
    path = list()
    # from tail to head
    head = tar
    # until head
    while True:
        path.append(head)
        if predecessor[name_to_id[head]] == None:
            break
        head = id_to_name[ predecessor[ name_to_id[head] ]]
    
    # reversed path
    path = list(reversed(path))
   
    # setup path output format 
    trajectory = ''
    for p in path:
        trajectory += p
        if p != path[-1]:
           trajectory += ' -- '

    # print path
    print(trajectory)
    # print distance from source(src) node to target(tar) node
    print(distance[ name_to_id[tar] ])

if __name__ == "__main__":
    main()
