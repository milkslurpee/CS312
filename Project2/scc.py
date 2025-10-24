import random
import sys
from time import time
import array
import string

GRAPH = dict[str, list[str]]
sys.setrecursionlimit(10000)

def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:
    visited = set()
    order = [0]
    prepost = []
    for node in graph:
        if node not in visited:
            tree = {}
            explore(node, graph, visited, order, tree)
            prepost.append(tree)
    return prepost

def explore(node, graph: GRAPH, visited, order, tree):
    visited.add(node)
    order[0] += 1
    preorder = order[0]
    for edge in graph[node]:
        if edge not in visited:
            explore(edge, graph, visited, order, tree)
    order[0] += 1
    postorder = order[0]
    tree[node] = [preorder, postorder]


def exploreSCCs(node, graph: GRAPH, visited, scc):
    visited.add(node)
    scc.add(node)
    for edge in graph[node]:
        if edge not in visited:
            exploreSCCs(edge, graph, visited, scc)


def find_sccs(graph: GRAPH) -> list[set[str]]:
    reverseGraph = reverse_graph(graph)
    reverseOrder = prepost(reverseGraph)
    postOrder = {}
    for dictionary in reverseOrder:
        for key, value in dictionary.items():
            postOrder[key] = value[1]
    dictionaryValues = postOrder.items()
    sortedDictionary = sorted(dictionaryValues, key=lambda x: x[1], reverse=True)
    sortedNodes = []

    for key, value in sortedDictionary:
        sortedNodes.append(key)

    SCCs = []
    visited = set()
    for node in sortedNodes:
        if node not in visited:
            scc = set()
            exploreSCCs(node, graph, visited, scc)
            SCCs.append(scc)
    return SCCs


def reverse_graph(graph: GRAPH) -> GRAPH:
    reversed_graph = {}
    for node in graph:
        for edge in graph[node]:
            if(edge not in reversed_graph):
                reversed_graph[edge] = []
            reversed_graph[edge].append(node)
    for node in graph:
        if node not in reversed_graph:
            reversed_graph[node] = []
    return reversed_graph

def classify_edges(graph: GRAPH, trees: list[dict[str, list[int]]]) -> dict[str, set[tuple[str, str]]]:
    """
    Return a dictionary containing sets of each class of edges
    """
    classification = {
        'tree/forward': set(),
        'back': set(),
        'cross': set()
    }

    return classification


