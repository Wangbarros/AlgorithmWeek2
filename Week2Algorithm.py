# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 15:58:30 2014

@author: chenwang
"""

import urllib2
import math
#import matplotlib
#import pylab
import random
from collections import Counter
from collections import deque

EX_GRAPH0 = {0: set([1,2]), 1:set([]), 2:set([])}
EX_GRAPH1 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3]), 3: set([0]), 4:set([1]), 5:set([2]), 6:set([])}
EX_GRAPH2 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3,7]), 3: set([7]), 4:set([1]), 5:set([2]), 6:set([]), 7:set([3]), 8:set([1,2]), 9:set([0,3,4,5,6,7])}

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
    """
    This function checkes the nodes that are visited by a bfs function
    
    """
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
    retorno = set(visited)
    return retorno
                
def cc_visited(digraph):
    """
    This function returns the groups of nodes
    
    """
    remaining = set(digraph.keys())
    retorno = []
    while remaining != set():
        node = (random.sample(remaining,1))[0]
        visited = (bfs_visited(digraph,node))
        remaining = remaining - visited
        retorno.append(visited)
    return (retorno)

def largest_cc_size(digraph):
    """
    This function returns the largest group visited
    
    """
    sizes = []
    groups = cc_visited(digraph)
    for seti in range(len(groups)):
        sizes.append(len(groups[seti]))
    sizes.sort()
    sizes.reverse()
    return sizes[0]
def compute_resilience(digraph, attack_order):
    """
    This function returns a list of largest conected groups after removing nodes in the attack list
    
    """
    sizes = []
    sizes.append(largest_cc_size(digraph))
    for node in (attack_order):
        for item in digraph.keys():
            if node in digraph[item]:
                digraph[item].remove(node)
        del digraph[node]
        if len(digraph) > 0:
            sizes.append(largest_cc_size(digraph))
        if len(digraph) == 0:
            sizes.append(0)
    return sizes