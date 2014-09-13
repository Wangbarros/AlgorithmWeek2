# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 15:58:30 2014

@author: chenwang
"""

import urllib2
import math
import matplotlib
import pylab
import random
from collections import Counter
from collections import deque

def make_complete_graph(num_nodes):
    """
    This function takes a number and returns a complete graph with that number of nodes
    
    """
    complete = {}
    for nodes in range(0, num_nodes):
        lista = range(num_nodes)
        lista.remove(nodes)
        complete[nodes] = set(lista)
    return complete    
def bfs_visited (digraph, node):
    queue = deque()
    visited = [node]
    queue.append(node)
    while queue != (deque()):
        jota = queue[0]
        queue.popleft()
        for neighbor in digraph[jota]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
    return visited
                
def cc_visited(ugraph):
    remaining = ugraph.keys
    CC = []
    while remaining != []:
        node = random.choice(remaining)
        W = bfs_visited(ugraph,node)
        CC.append(W)
        remaining.remove(node)
    return CC

def largest_cc_size(ugraph):
    return 0