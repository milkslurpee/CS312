import heapq


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
    """Heap-based priority queue using a binary heap with an auxiliary dictionary for fast lookups."""

    def __init__(self):
        self.heap = []  # List of tuples (distance, node)
        self.pointers = {}  # Maps nodes to their heap indices

    def makeQueue(self, graph, source):
        """Initialize the priority queue with all nodes set to infinity, except the source."""

        # This section of code iterates through all the nodes and sets their distances to infinity
        # and has a time complexity of O(n).

        for node in graph:
            if node == source:
                heapq.heappush(self.heap, (0, node))
                self.pointers[node] = 0
            else:
                heapq.heappush(self.heap, (float("inf"), node))
                self.pointers[node] = float("inf")

    def insert(self, node, distance):

        # This section of code inserts nodes into the binary heap priority queue.
        # This will take O(logn) time.

        heapq.heappush(self.heap, (distance, node))
        self.pointers[node] = distance

    def deleteMin(self):

        # This section of code extracts the minimum distance node from the binary heap priority queue.
        # In the binary heap implementation, deleteMin takes O(logn) time, and since it is called O(n) times,
        # the total contribution is O(nlogn).

        while self.heap:
            distance, node = heapq.heappop(self.heap)
            if node in self.pointers:
                del self.pointers[node]
                return node, distance
        return None, float("inf")

    def decreaseKey(self, node, new_distance):

        # This section of code updates the distance of a node in the binary heap.
        # Since heapq does not support direct updates, we push the updated value and rely on heap properties.
        # This results in an O(logn) time complexity per call.
        # Since decreaseKey is called at most O(e) times, its overall contribution is O(elogn).

        if node in self.pointers and new_distance < self.pointers[node]:
            self.pointers[node] = new_distance
            heapq.heappush(self.heap, (new_distance, node))


class ArrayPQ:

    def __init__(self):
        self.queue = {}  # Dictionary for direct lookup

    def makeQueue(self, graph, source):
        """Initialize the queue with all nodes set to infinity, except the source."""

        # This section of code iterates through all the nodes and sets their distances to infinity
        # and has a time complexity of O(n).

        for node in graph:
            self.queue[node] = float("inf")
        self.queue[source] = 0

    def insert(self, node, distance):

        # This section of code inserts nodes into the unsorted array priority queue.
        # In an unsorted array this has a constant time complexity as it is simply placed at the end of the array.

        self.queue[node] = distance

    def deleteMin(self):

        # This section of code extracts the minimum distance node from the unsorted array priority queue.
        # In the unsorted array implementation this operation has a time complexity of O(n).

        if not self.queue:
            return None, float("inf")
        node = min(self.queue, key=self.queue.get)
        return node, self.queue.pop(node)

    def decreaseKey(self, node, new_distance):

        # In an unsorted array, updating the key is O(1), but deleteMin is still O(n), so the overall impact remains O(n^2).

        if node in self.queue and new_distance < self.queue[node]:
            self.queue[node] = new_distance







def dijkstra(graph, source, target, use_heap=True):
    """
    Implements Dijkstra's algorithm using either a heap-based or array-based priority queue.
    """
    pq = HeapPQ() if use_heap else ArrayPQ()
    pq.makeQueue(graph, source)

    distances = {node: float("inf") for node in graph}
    distances[source] = 0
    previous_nodes = {node: None for node in graph}

    while True:
        current, current_dist = pq.deleteMin()
        if current is None or current_dist == float("inf"):
            break  # No more reachable nodes

        if current == target:
            break  # Reached target

        # This section of code examines all of the edges of all of the neighboring nodes
        # and sees if the distance between two neighbors can be shortened by going through the current node.
        # Since this requires examining all of the edges, this has a time complexity of O(e).

        for neighbor, weight in graph[current].items():
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous_nodes[neighbor] = current
                pq.decreaseKey(neighbor, new_dist)

    # Overall time complexity:
    # - Unsorted array: O(n^2) deleteMin is O(n) and it is called n times.
    # - Binary heap: O((n + e) logn) because deleteMin and decreaseKey both are O(logn) and they are called O(n + e) times.


    if distances[target] == float("inf"):
        return [], float("inf")

    # Reconstruct path
    path, node = [], target
    while node is not None:
        path.append(node)
        node = previous_nodes[node]
    path.reverse()

    return path, distances[target]