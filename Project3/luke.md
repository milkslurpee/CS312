# Project Report - Network Routing

## Baseline

### Design Experience

I talked with Jack

Discussion points:
- linear priority queue using dictionary
    - to `make_queue`, append nodes to pq with distance float('inf')
    - to `decrease key`, find node in pq and change key
    - to `delete min`, iterate through pq and pop highest priority node
- dijkstra's
    - set start node distance to 0, the rest to infinity
    - initialize pq with source=0 and others at float('inf'). update distances as nodes are found
    - pick next node to iterate from pq
    - update distance in pq if node's new distance < curr distance

### Theoretical Analysis - Dijkstra's With Linear PQ

#### Time 

```py
class LinearPQ():
    def __init__(self):
        self.queue = {}

    def make_queue(self, distance):
        self.queue = distance.copy()                # O(V) - work for every node

    def decrease_key(self, node: int, newWeight: float):
        self.queue[node] = newWeight                # O(1) - simple operation
        
    def delete_min(self):
        lowestNode = None
        lowestVal = float('inf')
        for node in self.queue.keys():              # O(V) - iterate through all nodes to find min
            if (self.queue[node] < lowestVal):      # O(1) - does simple operation if true
                lowestNode = node
                lowestVal = self.queue[node]
        if lowestNode != None:                      # O(1)
            self.queue.pop(lowestNode)
        return lowestNode
--------------------------------------------------
def dijkstras(graph, source, target, useHeap):
    distance = {node: float('inf') for node in graph.keys()}    # O(V) - add every node to distance map
    prev = {node: None for node in graph.keys()}                # O(V) - add every node to prev map
    distance[source] = 0
    if useHeap:
        pq = HeapPQ()
    else: pq = LinearPQ()
    pq.make_queue(distance)                                     #O(V) - see make_queue
    while pq.queue:                                             #O(V) - will execute a max of n times
        node = pq.delete_min()                                  #O(V) - see delete_min
        if node == None or node == target:                      #O(1) - breaks loop if target found or no more valid nodes to explore
            break
        for edge in graph[node].keys():                         #O(E) - runs for every edge connected to node.
            newDistance = distance[node] + graph[node][edge]
            if newDistance < distance[edge]:
                pq.decrease_key(edge, newDistance)              #O(1) - updates edge node in map
                distance[edge] = newDistance
                prev[edge] = node
    if distance[target] == float('inf'):
        return [], float('inf')
    else:
        path = [target]
        curr = target
        while curr != source:                                   #O(V) - path could be up to n nodes long
            path.append(prev[curr])
            curr = prev[curr]
        path.reverse()                                          #O(V) - python list reversal
        return path, distance[target]
```
Dijkstras has a time big O of O(V^2 + E). Inside the while loop, which can iterate over every node, `delete_min` iterates over every node and `for edge in graph[node].keys()` iterates over every edge. However, the edge loop does NOT execute V*E times. It executes E times overall because it only runs in the presence of an edge.

#### Space

```py
class LinearPQ():
    def __init__(self):
        self.queue = {}

    def make_queue(self, distance):
        self.queue = distance.copy()                # O(V) - stores every node

    def decrease_key(self, node: int, newWeight: float):
        self.queue[node] = newWeight
        
    def delete_min(self):
        lowestNode = None                           #O(1)
        lowestVal = float('inf')                    #O(1)
        for node in self.queue.keys():
            if (self.queue[node] < lowestVal):
                lowestNode = node
                lowestVal = self.queue[node]
        if lowestNode != None:
            self.queue.pop(lowestNode)
        return lowestNode
--------------------------------------------------
def dijkstras(graph, source, target, useHeap):
    distance = {node: float('inf') for node in graph.keys()}    # O(V) - store distance for every node
    prev = {node: None for node in graph.keys()}                # O(V) - store prev for every node
    distance[source] = 0
    if useHeap: pq = HeapPQ()                                   #O(1) - initializes empty pq
    else: pq = LinearPQ()
    pq.make_queue(distance)                                     #O(V) - copies distance map to pq.queue
    while pq.queue:                                             #O(1) - from this point on, nothing new is permanently stored, values are only updated or removed
        node = pq.delete_min()                                  #O(-1) - removes one node from pq.queue
        if node == None or node == target:
            break
        for edge in graph[node].keys():
            newDistance = distance[node] + graph[node][edge]    #O(1) - stores newDistance, but only in loop scope
            if newDistance < distance[edge]:
                pq.decrease_key(edge, newDistance)              #O(1) - updates value
                distance[edge] = newDistance                    #O(1) - updates value
                prev[edge] = node                               #O(1) - updates value
    if distance[target] == float('inf'):
        return [], float('inf')
    else:
        path = [target]
        curr = target
        while curr != source:                                   #O(V) - stored path could be up to V nodes long
            path.append(prev[curr])
            curr = prev[curr]
        path.reverse()                                          #O(1) - python list reverse modifies list in place
        return path, distance[target]
```
The space complexity for Dijkstras is O(V). Distance, prev, and queue placement are initialized for each node and are updated as the algorithm runs.

### Empirical Data - Dijkstra's With Linear PQ

Distribution: **uniform**
Density: **0.3**
Noise: **0.05**
PQ Implementation: **Linear**

|    V    |    E      | Time (sec) |
| ------- | --------- | ---------- |
| 500     | 75000.0   | 0.016      |
| 1000    | 300000.0  | 0.068      |
| 1500    | 675000.0  | 0.16       |
| 2000    | 1200000.0 | 0.301      |
| 2500    | 1875000.0 | 0.539      |
| 3000    | 2700000.0 | 0.665      |
| 3500    | 3675000.0 | 1.001      |

### Comparison of Theoretical and Empirical Results - Dijkstra's With Linear PQ

- Theoretical order of growth: O(v^2 + e)
- Empirical order of growth (if different from theoretical): same 

![img](_analysis/empirical1.svg)
![img](_analysis/empirical2.svg)

Empirical runtime was far lower than theoretical. However, when I divide the theoretical runtime by 5 million, it follows empirical results quite closely. I suspect this is due to the computer handling processes far faster than expected, but still doing O(v^2 + e) work.

## Core

### Design Experience

I talked with Jack.

Discussion points:
- dijkstra's logic remains the same, refactor to it's own function to prevent redundancy. use boolean to decide between linear and heap.
- heap priority queue using array
    - self.queue stores list of [node, distance] values
    - self.index stores maps node -> index in queue
    - `make_queue`: for node, append to queue and bubble up
    - `bubble_up`: for node location in queue, compare weight to parent and swap if higher priority
    - `sift_down`: for node location in queue, compare weight to child and swap if lower priority
    - `decrease_key`: update node weight in queue, then bubble up
    - `delete_min`: swap first and last, update indexes, pop last (which is actually first). this prevents shifting other indices to fill empty space.

### Theoretical Analysis - Dijkstra's With Heap PQ

#### Time 

```py
class HeapPQ():
    def __init__(self):
        self.queue = []
        self.index = {}

    def bubble_up(self, index):
        while True:                     # O(log V) - this can run until the node is at the top of the queue
            if index == 0: break
            parent = (index-1) // 2
            if self.queue[index][1] < self.queue[parent][1]:
                self.queue[index], self.queue[parent] = self.queue[parent], self.queue[index]   #O(1)
                self.index[self.queue[index][0]] = index                                        #O(1)
                self.index[self.queue[parent][0]] = parent                                      #O(1)
                index = parent                                                                  #O(1)
            else: break

    def sift_down(self, index):
        while True:                     # O(log V) - this can run until the node is at the bottom layer of the queue
            child1 = (index * 2) + 1
            child2 = (index * 2) + 2
            if child1 > len(self.queue)-1:
                break
            elif child2 > len(self.queue)-1:
                favChild = child1
            elif self.queue[child1][1] <= self.queue[child2][1]:
                favChild = child1
            else: 
                favChild = child2

            if self.queue[index][1] > self.queue[favChild][1]:
                self.queue[index], self.queue[favChild] = self.queue[favChild], self.queue[index]   #O(1)
                self.index[self.queue[index][0]] = index                                            #O(1)
                self.index[self.queue[favChild][0]] = favChild                                      #O(1)
                index = favChild                                                                    #O(1)
            else: break

    def make_queue(self, distance):
        for node in distance:                           #O(V) - runs for every node
            self.queue.append([node, distance[node]])   #O(1)
            self.index[node] = len(self.queue) - 1      #O(1)
            self.bubble_up(len(self.queue)-1)           #O(log V) - see bubble_up

    def decrease_key(self, node: int, newDistance: float):
        self.queue[self.index[node]] = [node, newDistance]  #O(1)
        self.bubble_up(self.index[node])                    #O(log V) - see bubble up

    def delete_min(self):
        if len(self.queue) == 0:
            return None
        if len(self.queue) == 1:
            min = self.queue.pop()[0]       #O(1)
            self.index.pop(min)             #O(1)
            return min
        self.queue[0], self.queue[len(self.queue)-1] = self.queue[len(self.queue)-1], self.queue[0] #O(1)
        min = self.queue.pop()[0]           #O(1)
        self.index[self.queue[0][0]] = 0    #O(1)
        self.index.pop(min)                 #O(1)
        self.sift_down(0)                   #O(log V) - see sift_down
        return min
----------------------------------------------------------
def dijkstras(graph, source, target, useHeap):
    distance = {node: float('inf') for node in graph.keys()}    # O(V) - add every node to distance map
    prev = {node: None for node in graph.keys()}                # O(V) - add every node to prev map
    distance[source] = 0
    if useHeap:
        pq = HeapPQ()
    else: pq = LinearPQ()
    pq.make_queue(distance)                                     #O(V log V) - see make_queue
    while pq.queue:                                             #O(V) - will execute a max of n times
        node = pq.delete_min()                                  #O(log V) - iterates through pq.queue to find min
        if node == None or node == target:                      #O(1) - breaks loop if target found or no more valid nodes to explore
            break
        for edge in graph[node].keys():                         #O(E) - runs for every edge connected to node.
            newDistance = distance[node] + graph[node][edge]
            if newDistance < distance[edge]:
                pq.decrease_key(edge, newDistance)              #O(log V) - updates edge node in map
                distance[edge] = newDistance
                prev[edge] = node
    if distance[target] == float('inf'):
        return [], float('inf')
    else:
        path = [target]
        curr = target
        while curr != source:                                   #O(V) - path could be up to n nodes long
            path.append(prev[curr])
            curr = prev[curr]
        path.reverse()                                          #O(V) - python list reversal
        return path, distance[target]
```
Time complexity is O(VlogV + ElogV). This is due to O(V log V) work of make_queue and the O(log V) work of `delete_min` inside the queue loop PLUS the O(log V) work of `decrease_key` inside the edge loop.

#### Space

```py
class HeapPQ():
    def __init__(self):
        self.queue = []
        self.index = {}

    def bubble_up(self, index):
        while True:
            if index == 0: break
            parent = (index-1) // 2     #O(1) - temporary value stored
            if self.queue[index][1] < self.queue[parent][1]:    #O(1) - only swaps occur
                self.queue[index], self.queue[parent] = self.queue[parent], self.queue[index]
                self.index[self.queue[index][0]] = index
                self.index[self.queue[parent][0]] = parent
                index = parent
            else: break

    def sift_down(self, index):
        while True:
            child1 = (index * 2) + 1    #O(1) - temporary value stored
            child2 = (index * 2) + 2    #O(1) - temporary value stored
            if child1 > len(self.queue)-1:
                break
            elif child2 > len(self.queue)-1:
                favChild = child1
            elif self.queue[child1][1] <= self.queue[child2][1]:
                favChild = child1
            else: 
                favChild = child2

            if self.queue[index][1] > self.queue[favChild][1]:  #O(1) - only swaps occur
                self.queue[index], self.queue[favChild] = self.queue[favChild], self.queue[index]
                self.index[self.queue[index][0]] = index
                self.index[self.queue[favChild][0]] = favChild
                index = favChild
            else: break

    def make_queue(self, distance):
        for node in distance:   # O(V) - stores every node queue and index
            self.queue.append([node, distance[node]])
            self.index[node] = len(self.queue) - 1  #O(1)
            self.bubble_up(len(self.queue)-1)   #O(1)

    def decrease_key(self, node: int, newDistance: float):
        self.queue[self.index[node]] = [node, newDistance]  #O(1) - only updating value
        self.bubble_up(self.index[node])    #O(1)

    def delete_min(self):
        if len(self.queue) == 0:
            return None
        if len(self.queue) == 1:
            min = self.queue.pop()[0]   #O(1)
            self.index.pop(min)
            return min
        self.queue[0], self.queue[len(self.queue)-1] = self.queue[len(self.queue)-1], self.queue[0]
        min = self.queue.pop()[0]   #O(1)
        self.index[self.queue[0][0]] = 0    #O(1)
        self.index.pop(min)
        self.sift_down(0)   #O(1)
        return min
--------------------------------------------------
def dijkstras(graph, source, target, useHeap):
    distance = {node: float('inf') for node in graph.keys()}    # O(V) - store distance for every node
    prev = {node: None for node in graph.keys()}                # O(V) - store prev for every node
    distance[source] = 0
    if useHeap: pq = HeapPQ()                                   #O(1) - initializes empty pq
    else: pq = LinearPQ()
    pq.make_queue(distance)                                     #O(V) - copies distance map to pq.queue
    while pq.queue:                                             #O(1) - from this point on, nothing new is permanently stored, values are only updated or removed
        node = pq.delete_min()                                  #O(-1) - removes one node from pq.queue
        if node == None or node == target:
            break
        for edge in graph[node].keys():
            newDistance = distance[node] + graph[node][edge]    #O(1) - stores newDistance, but only in loop scope
            if newDistance < distance[edge]:
                pq.decrease_key(edge, newDistance)              #O(1) - updates value
                distance[edge] = newDistance                    #O(1) - updates value
                prev[edge] = node                               #O(1) - updates value
    if distance[target] == float('inf'):
        return [], float('inf')
    else:
        path = [target]
        curr = target
        while curr != source:                                   #O(V) - stored path could be up to V nodes long
            path.append(prev[curr])
            curr = prev[curr]
        path.reverse()                                          #O(1) - python list reverse modifies list in place
        return path, distance[target]
```
Space complexity is O(V). This is the same as with the linear implementation because everything stored is still relative to the number of nodes.
### Empirical Data - Dijkstra's With Heap PQ

Distribution: **uniform**
Density: **0.3**
Noise: **0.05**
PQ Implementation: **Heap**

|    V    |    E      | Time (sec) |
| ------- | --------- | ---------- |
| 500     | 75000.0   | 0.01       |
| 1000    | 300000.0  | 0.048      |
| 1500    | 675000.0  | 0.118      |
| 2000    | 1200000.0 | 0.211      |
| 2500    | 1875000.0 | 0.338      |
| 3000    | 2700000.0 | 0.471      |
| 3500    | 3675000.0 | 0.691      |


### Comparison of Theoretical and Empirical Results - Dijkstra's With Heap PQ

- Theoretical order of growth: O(VlogV + ElogV)
- Empirical order of growth (if different from theoretical): same

![img](_analysis/empirical3.svg)
![img](_analysis/empirical4.svg)

Empirical runtime was far lower than theoretical. However, when I divide the theoretical runtime by 20 million, it follows empirical results quite closely. I suspect this is due to the computer handling processes far faster than expected, but still doing O(VlogV + ElogV) work.

### Relative Performance Of Linear versus Heap PQ Performance

The Heap PQ performed better in my tests, with runtimes generally around 60-70% as long as Linear PQ's. At this density, the O(logV) work done in `bubble_up` and `sift_down` is less than the work done by Linear PQ's `delete_min` O(V). However, as density increases, increased calls of `bubble_up` and `sift_down` functions may overtake the work done in the linear `delete_min` with it's static queue implementation.

## Stretch 1

### Design Experience

*Fill me in*

### Empirical Data

| N    | Density | heap time (ms) | linear PQ time (ms) |
|------|---------|----------------|---------------------|
| 500  | .6      |                |                     |
| 1000 | .6      |                |                     |
| 1500 | .6      |                |                     |
| 2000 | .6      |                |                     |
| 2500 | .6      |                |                     |
| 3000 | .6      |                |                     |
| 3500 | .6      |                |                     |


| N    | Density | heap time (ms) | linear PQ time (ms) |
|------|---------|----------------|---------------------|
| 500  | 1       |                |                     |
| 1000 | 1       |                |                     |
| 1500 | 1       |                |                     |
| 2000 | 1       |                |                     |
| 2500 | 1       |                |                     |
| 3000 | 1       |                |                     |
| 3500 | 1       |                |                     |

### Plot

*Fill me in*

### Discussion

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*

### Provided Graph Generation Algorithm Explanation

*Fill me in*

### Selected Graph Generation Algorithm Explanation

*Fill me in*

#### Screenshots of Working Graph Generation Algorithm

![img](small.png)

![img](medium.png)

![img](large.png)

## Project Review

*Fill me in*