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


def find_sccs(graph: GRAPH) -> list[set[str]]:
    """
    Return a list of the strongly connected components in the graph.
    The list should be returned in order of sink-to-source
    """
    return []


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


