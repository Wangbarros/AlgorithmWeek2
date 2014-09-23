# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 15:58:30 2014

@author: chenwang
"""

import urllib2
import math
import matplotlib
import pylab
import time
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

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
##########################################################
# Code for loading computer network graph

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph
    
def UER(n,p):
    
    graph = {} 
    for i in range(0,n):
        graph[i] = set([])
    for i in range(0, n):
        for j in range(0,n):
            if j != i:
                a = random.random()
                if a<p:
                    graph[i].update([j])
                    graph[j].update([i])
    return graph
    
class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def random_order(ugraph):
    keys = ugraph.keys()
    random.shuffle(keys)
    
    return keys
    
def count_edges(ugraph):
    count = 0
    for node in range(len(ugraph)):
        count = count + len(ugraph[node])
    return count/2 

def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order   

def fast_targeted_order(ugraph):
    new_graph = copy_graph(ugraph)
    DegreeSets = degree_sets(new_graph)
    L = []   
    for k in range(len(new_graph)-1,0,-1):
        while DegreeSets[k] != set():
             u = random.sample(DegreeSets[k],1)
             DegreeSets[k].remove(u[0])
             for neighbor in new_graph[u[0]]:
                 d = len(new_graph[neighbor])
                 DegreeSets[d].remove(neighbor)
                 DegreeSets[d-1].update([neighbor])
             L.append(u[0])
             delete_node(new_graph,u[0])
    return L
    
def degree_sets(ugraph):
    DegreeSets = {}
    degree = []
    for node in range(0,len(ugraph)):
        degree.append(len(ugraph[node]))
    for k in range(0, len(degree)):
        indexes = [i for i,x in enumerate(degree) if x == k]
        DegreeSets[k] = set(indexes)
    return DegreeSets
    
    
NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
m = 5
edges = 3112
n = 1347
complete = make_complete_graph(m)
U = UPATrial(m)
for i in range(m,n):
    if i not in complete.keys():
        complete[i] = set()
    b = U.run_trial(m)
    complete[i].update(list(b))
    for item in b:
        complete[item].update([i])
computer = load_graph(NETWORK_URL)
ER = UER(n,0.001725)

computer_resilience = compute_resilience(computer, random_order(computer))
upa_resilience = compute_resilience(complete, random_order(complete))
er_resilience = compute_resilience(ER, random_order(ER))
y = range(0,1347)

fig = matplotlib.pyplot.figure()
matplotlib.pyplot.plot(computer_resilience, 'bo', label="computer network")
matplotlib.pyplot.plot(upa_resilience, 'ro', label = "UPA;m = 5;n=1347")
matplotlib.pyplot.plot(er_resilience, 'go', label = "UER;n=1347;p=0.001725")
fig.suptitle("Graphs resilience")
matplotlib.pyplot.xlabel("Nodes removed")
matplotlib.pyplot.ylabel("Largest coneected component")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()

m = 5
time_target = []
time_fast = []
for n in range(10,1000,10):
    ugraph = make_complete_graph(m)
    U = UPATrial(m)
    for i in range(m,n):
        if i not in ugraph.keys():
            ugraph[i] = set()
        b = U.run_trial(m)
        ugraph[i].update(list(b))
        for item in b:
            ugraph[item].update([i])
                
    start_time = time.time()
    a = targeted_order(ugraph)
    end_time = time.time()
    
    start_time2 = time.time()
    b = fast_targeted_order(ugraph)
    end_time2 = time.time()
    
    time_target.append(end_time - start_time)
    time_fast.append(end_time2 - start_time2)
    
    
    
    
    
    
    
    
