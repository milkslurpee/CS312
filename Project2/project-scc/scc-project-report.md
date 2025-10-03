# Project Report - Network Analysis SCCs

## Baseline

### Design Experience

I talked with my brother Luke about the design of the prepost function
Discussion Points

    - Iterate through nodes in graph that haven't been visited, calling explore on each one
    - Recursively explore edge nodes that haven't been visited
    - Mark node as visited, and increment pre and post order of each node accordingly
    - Return dictionaries containing the pre and post order of each node.

### Theoretical Analysis - Pre/Post Order Traversal

#### Time 
```py
def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:
    visited = set()
    order = [0]
    prepost = []
    for node in graph:                                          # Time: O(|V|) we make sure we visit all nodes
        if node not in visited:
            tree = {}
            explore(node, graph, visited, order, tree)                              
            prepost.append(tree)
    return prepost

def explore(node, graph: GRAPH, visited, order, tree):
    visited.add(node)
    order[0] += 1
    preorder = order[0]
    for edge in graph[node]:                                    # O(|E|) we explore all edges of graph, visiting nodes which haven't been visited yet
        if edge not in visited:
            explore(edge, graph, visited, order, tree)
    order[0] += 1
    postorder = order[0]
    tree[node] = [preorder, postorder]
```

The time complexity of Prepost is O(|V|+|E|). Even though explore, which has O(|E|), is called inside a 
for-loop which iterates through all nodes, the explore function also visits nodes, marking them visited, so
they aren't visited by the outer for-loop. The loop is only there to catch nodes that are completely
isolated from others.

#### Space

```py
def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:
    visited = set()
    order = [0]
    prepost = []
    for node in graph:                                         
        if node not in visited:
            tree = {}
            explore(node, graph, visited, order, tree)                              
            prepost.append(tree)                                # O(|V|) We are only saving the pre and post order of each node
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
```

The Space complexity is O(|V|) since we are only saving the pre and post order of nodes. Even though we iterate 
through edges, we only do so to visit nodes and get their pre and post order. As we visit edges, their order is saved
and the number of nodes we must iterate through in the for-loop decreased.

### Empirical Data

| Density Factor | Size  |    V    |    E    | Time (sec) |
| -------------- | ----- | ------- | ------- | ---------- |
| 0.25           | 10    | 10.0    | 12.8    | 0.0        |
| 0.25           | 50    | 50.0    | 61.6    | 0.0        |
| 0.25           | 100   | 100.0   | 123.5   | 0.0        |
| 0.25           | 500   | 500.0   | 616.1   | 0.0        |
| 0.25           | 1000  | 1000.0  | 1242.3  | 0.001      |
| 0.25           | 2000  | 2000.0  | 2496.5  | 0.001      |
| 0.25           | 4000  | 4000.0  | 4982.6  | 0.002      |
| 0.25           | 8000  | 8000.0  | 9967.0  | 0.005      |
| 0.5            | 10    | 10.0    | 17.7    | 0.0        |
| 0.5            | 50    | 50.0    | 85.2    | 0.0        |
| 0.5            | 100   | 100.0   | 173.1   | 0.0        |
| 0.5            | 500   | 500.0   | 872.2   | 0.0        |
| 0.5            | 1000  | 1000.0  | 1770.4  | 0.001      |
| 0.5            | 2000  | 2000.0  | 3551.4  | 0.001      |
| 0.5            | 4000  | 4000.0  | 7147.2  | 0.002      |
| 0.5            | 8000  | 8000.0  | 14361.9 | 0.005      |
| 1              | 10    | 10.0    | 24.5    | 0.0        |
| 1              | 50    | 50.0    | 134.1   | 0.0        |
| 1              | 100   | 100.0   | 272.5   | 0.0        |
| 1              | 500   | 500.0   | 1429.5  | 0.0        |
| 1              | 1000  | 1000.0  | 2921.5  | 0.001      |
| 1              | 2000  | 2000.0  | 5928.1  | 0.001      |
| 1              | 4000  | 4000.0  | 12010.6 | 0.003      |
| 1              | 8000  | 8000.0  | 24327.1 | 0.005      |
| 2              | 10    | 10.0    | 36.1    | 0.0        |
| 2              | 50    | 50.0    | 239.4   | 0.0        |
| 2              | 100   | 100.0   | 499.2   | 0.0        |
| 2              | 500   | 500.0   | 2710.2  | 0.0        |
| 2              | 1000  | 1000.0  | 5589.5  | 0.001      |
| 2              | 2000  | 2000.0  | 11450.9 | 0.001      |
| 2              | 4000  | 4000.0  | 23462.8 | 0.003      |
| 2              | 8000  | 8000.0  | 47740.4 | 0.007      |
| 3              | 10    | 10.0    | 46.0    | 0.0        |
| 3              | 50    | 50.0    | 356.9   | 0.0        |
| 3              | 100   | 100.0   | 766.3   | 0.0        |
| 3              | 500   | 500.0   | 4321.3  | 0.0        |
| 3              | 1000  | 1000.0  | 8788.2  | 0.001      |
| 3              | 2000  | 2000.0  | 17810.6 | 0.002      |
| 3              | 4000  | 4000.0  | 36212.5 | 0.004      |
| 3              | 8000  | 8000.0  | 73442.4 | 0.008      |


### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: O(|V|+|E|) 
- Empirical order of growth (if different from theoretical): 

![img](img.png)

*Fill me in*

## Core

### Design Experience

*Fill me in*

### Theoretical Analysis - SCC

#### Time 

*Fill me in*

#### Space

*Fill me in*

### Empirical Data


| density factor | size  | V | E | runtime |
|----------------|-------|---|---|---------|
| 0.25           | 10    |   |   |         |
| 0.25           | 50    |   |   |         |
| 0.25           | 100   |   |   |         |
| 0.25           | 500   |   |   |         |
| 0.25           | 2000  |   |   |         |
| 0.25           | 4000  |   |   |         |
| 0.25           | 80000 |   |   |         |
| 0.5            | 10    |   |   |         |
| 0.5            | 50    |   |   |         |
| 0.5            | 100   |   |   |         |
| 0.5            | 500   |   |   |         |
| 0.5            | 2000  |   |   |         |
| 0.5            | 4000  |   |   |         |
| 0.5            | 8000  |   |   |         |
| 1              | 10    |   |   |         |
| 1              | 50    |   |   |         |
| 1              | 100   |   |   |         |
| 1              | 500   |   |   |         |
| 1              | 2000  |   |   |         |
| 1              | 4000  |   |   |         |
| 1              | 8000  |   |   |         |
| 2              | 10    |   |   |         |
| 2              | 50    |   |   |         |
| 2              | 100   |   |   |         |
| 2              | 500   |   |   |         |
| 2              | 2000  |   |   |         |
| 2              | 4000  |   |   |         |
| 2              | 8000  |   |   |         |
| 3              | 10    |   |   |         |
| 3              | 50    |   |   |         |
| 3              | 100   |   |   |         |
| 3              | 500   |   |   |         |
| 3              | 2000  |   |   |         |
| 3              | 4000  |   |   |         |
| 3              | 8000  |   |   |         |



### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: *copy from section above* 
- Empirical order of growth (if different from theoretical): 

![img](img.png)

*Fill me in*

## Stretch 1

### Design Experience

*Fill me in*

### Articulation Points Discussion 

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*

### Dataset Description

*Fill me in*

### Findings Discussion

*Fill me in*

## Project Review

*Fill me in*
