import itertools
from heapq import *

class PriorityQueue(object):

    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = itertools.count()     # unique sequence count

    def __str__(self):
        return str([entry for entry in self.pq if entry[2] != self.REMOVED])

    def _add(self, task, in_edge, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task, in_edge]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def _remove(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def _pop(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task, in_edge = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task, in_edge, priority
        raise KeyError('pop from an empty priority queue')

    def size(self):
        return len([entry for entry in self.pq if entry[2] != self.REMOVED])

    
