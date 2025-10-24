def find_shortest_path_with_heap(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    return dijkstra(graph, source, target, use_heap=True)
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """


def find_shortest_path_with_linear_pq(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    return dijkstra(graph, source, target, use_heap=False)
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """


class HeapPQ:
    def __init__(self):
        self.heap = []  # List of tuples (distance, node)
        self.pointers = {}  # Maps nodes to their heap indices

    def makeQueue(self, distances):
        for node, dist in distances.items():
            self.insert(node, dist)

    def bubble_up(self, current):
        parent = (current - 1) // 2
        if current > 0 and self.heap[current][0] < self.heap[parent][0]:
            currentNode = self.heap[current][1]
            parentNode = self.heap[parent][1]
            self.heap[current], self.heap[parent] = self.heap[parent], self.heap[current]
            self.pointers[currentNode], self.pointers[parentNode] = parent, current
            self.bubble_up(parent)


    def bubble_down(self, current):
        child1 = current * 2 + 1
        child2 = current * 2 + 2
        favchild = child1
        if favchild >= len(self.heap):
            return
        if child2 < len(self.heap):
            if self.heap[child1][0] > self.heap[child2][0]:
                favchild = child2
        if self.heap[favchild][0] > self.heap[current][0]:
            return
        self.heap[favchild], self.heap[current] = self.heap[current], self.heap[favchild]
        currentNode = self.heap[favchild][1]
        childNode = self.heap[current][1]
        self.pointers[currentNode], self.pointers[childNode] = favchild, current
        self.bubble_down(favchild)

    def insert(self, node, distance):
        self.heap.append((distance, node))
        current = len(self.heap) - 1
        self.pointers[node] = current
        self.bubble_up(current)

    def deleteMin(self):
        if self.heap:
            dist, node = self.heap[0]
            if len(self.heap) == 1:
                self.heap.pop()
                del self.pointers[node]
                return node, dist

            self.heap[0] = self.heap.pop()
            self.pointers[self.heap[0][1]] = 0
            del self.pointers[node]
            self.bubble_down(0)
            return node, dist




    def decreaseKey(self, node, new_distance):
        index = self.pointers[node]
        if node in self.pointers and new_distance < self.heap[index][0]:
            self.heap[index] = (new_distance, node)
            self.bubble_up(index)


class LinearPQ:

    def __init__(self):
        self.queue = {}

    def makeQueue(self, distances):
        self.queue = distances.copy()

    def deleteMin(self):
        if not self.queue:
            return None, float("inf")
        node = min(self.queue, key=self.queue.get)
        return node, self.queue.pop(node)

    def decreaseKey(self, node, new_distance):
        if node in self.queue and new_distance < self.queue[node]:
            self.queue[node] = new_distance







def dijkstra(graph, source, target, use_heap=True):
    pq = HeapPQ() if use_heap else LinearPQ()

    distances = {node: float("inf") for node in graph}
    distances[source] = 0
    previous_nodes = {node: None for node in graph}

    pq.makeQueue(distances)

    while True:
        current, current_dist = pq.deleteMin()
        if current is None or current_dist == float("inf"):
            break  # No more reachable nodes

        if current == target:
            break  # Reached target

        for neighbor, weight in graph[current].items():
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous_nodes[neighbor] = current
                pq.decreaseKey(neighbor, new_dist)

    if distances[target] == float("inf"):
        return [], float("inf")

    path, node = [], target
    while node is not None:
        path.append(node)
        node = previous_nodes[node]
    path.reverse()

    return path, distances[target]
