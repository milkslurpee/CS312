import math
import random
import heapq
from Project7.reduce_cost import reduced_matrix
from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree

PARAMS_FOR_SMART_BRANCH_AND_BOUND_SMART_TEST = {
    "n": 30,
    "euclidean": True,
    "reduction": 0.2,
    "normal": False,
    "seed": 312,
    "timeout" : 20
}

def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]

def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:

    stats = []
    best_score = math.inf
    for start_city in range(len(edges)):
        tour = [start_city]
        current_city = start_city

        while True:
            if timer.time_out():
                return stats
            closest_city = None
            closest_city_cost = math.inf
            for neighboring_city in range(len(edges[current_city])):
                if neighboring_city in tour:
                    continue
                neighbor_cost = edges[current_city][neighboring_city]
                if neighbor_cost < closest_city_cost:
                    closest_city = neighboring_city
                    closest_city_cost = neighbor_cost

            if closest_city is None:
                break

            current_city = closest_city
            tour.append(closest_city)

            if len(tour) == len(edges):
                score = score_tour(tour, edges)
                if score < best_score:
                    best_score = score
                    stats.append(SolutionStats(
                        tour=tour,
                        score=best_score,
                        time=timer.time(),
                        max_queue_size=0,
                        n_nodes_expanded=0,
                        n_nodes_pruned=0,
                        n_leaves_covered=0,
                        fraction_leaves_covered=0
                    ))
                break

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            0,
            0,
            0,
            0
        )]
    else: return stats


def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stack = [[0]]
    stats = []
    best_score = math.inf
    while stack and not timer.time_out():       #O(n^2) the stack can
        tour = stack.pop()
        previous = tour[-1]

        if len(tour) == len(edges):
            score = score_tour(tour, edges)
            if score < best_score:
                best_score = score
                best_tour = tour
                stats.append(SolutionStats(
                    tour=best_tour,
                    score = best_score ,
                    time=timer.time(),
                    max_queue_size=1,
                    n_nodes_expanded=0,
                    n_nodes_pruned=0,
                    n_leaves_covered=0,
                    fraction_leaves_covered=0
                ))

        for neighboring_city in range(0, len(edges)):

            if neighboring_city in tour or edges[previous][neighboring_city] == math.inf:
                continue

            new_path = tour.copy()
            new_path.append(neighboring_city)
            stack.append(new_path)

    if stats: return stats
    else:   return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            0,
            0,
            0,
            0
        )]


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    # Initialize reduced matrix and lower bound
    starting_matrix, lower_bound = reduce_matrix(edges)
    upper_bound = math.inf
    best_tour = None

    # Root node setup
    root = Node(
        matrix=starting_matrix,
        bound=lower_bound,
        included_set=set(),  # No edges forced yet
        included_list=[],  # Track the list of edges in the tour
        excluded_edges=set(),  # No edges excluded yet
        parent=None  # No parent for root
    )

    pq = []
    heapq.heappush(pq, root)

    total_nodes_expanded = 1
    total_nodes_pruned = 0
    max_queue_size = 1
    stats = None  # To store the best result

    # Start the branch and bound process
    while pq and not timer.time_out():
        current_node = heapq.heappop(pq)

        # Prune node if its bound is greater than or equal to the upper bound
        if current_node.bound >= upper_bound:
            total_nodes_pruned += 1
            continue

        # Check if a complete tour has been formed
        if len(current_node.included_set) == len(edges):
            # Reconstruct the tour from the included edges
            tour = reconstruct_tour(current_node.included_list, len(edges))
            if tour is not None:  # Valid complete tour
                # Calculate the cost of the current tour
                tour_cost = score_tour(tour, edges)
                if tour_cost < upper_bound:
                    upper_bound = tour_cost
                    best_tour = tour
                    # Store stats for the best solution found
                    stats = SolutionStats(
                        tour=best_tour,
                        score=upper_bound,
                        time=timer.time(),
                        max_queue_size=len(pq),
                        n_nodes_expanded=total_nodes_expanded,
                        n_nodes_pruned=total_nodes_pruned,
                        n_leaves_covered=len(current_node.included_set),
                        fraction_leaves_covered=len(current_node.included_set) / (len(edges) - 1),
                    )
            continue  # Continue processing if a complete tour is found

        # Otherwise, perform branching (find edges to include/exclude)
        n = len(current_node.matrix)
        for i in range(n):
            for j in range(n):
                if current_node.matrix[i][j] == 0:  # Find candidate edges for branching
                    if (i, j) not in current_node.included_set and (i, j) not in current_node.excluded_edges:
                        # Create a new node for this branch
                        new_node = Node(
                            matrix=[row[:] for row in current_node.matrix],  # Copy the matrix
                            bound=current_node.bound,  # Update the bound if necessary
                            included_set=current_node.included_set.copy(),  # Include edge
                            included_list=current_node.included_list.copy(),
                            excluded_edges=current_node.excluded_edges.copy(),
                            parent=current_node
                        )
                        new_node.add_included_edge((i, j))  # Add the current edge

                        # Apply matrix reduction and update the bound after including the edge
                        new_node.matrix, new_node.bound = reduce_matrix(new_node.matrix)

                        # Push the new node to the priority queue
                        heapq.heappush(pq, new_node)
                        total_nodes_expanded += 1

    # If a best solution was found, return it, else return an empty solution
    return [stats] if stats else [
        SolutionStats([], math.inf, timer.time(), 1, total_nodes_expanded, total_nodes_pruned, 0, 0)]


def reconstruct_tour(edge_list, n):
    adj = [[] for _ in range(n)]
    for i, j in edge_list:
        adj[i].append(j)
        adj[j].append(i)

    for i in range(n):
        if len(adj[i]) != 2:
            return None
    tour = [0]
    current, previous = 0, -1

    while len(tour) < n:
        if adj[current][0] == previous:
            next_city = adj[current][1]
        else:
            next_city = adj[current][0]

        tour.append(next_city)
        previous = current
        current = next_city
    if adj[tour[-1]][0] != 0 and adj[tour[-1]][1] != 0:
        return None
    return tour


class Node:
    def __init__(self, matrix, bound, included_set=None, included_list=None, excluded_edges=None, parent=None):
        self.matrix = [row[:] for row in matrix]  # Deep copy of matrix
        self.bound = bound  # Lower bound for this node
        self.included_set = included_set or set()  # Set of included edges
        self.included_list = included_list or []  # List of edges in the tour
        self.excluded_edges = excluded_edges or set()  # Set of excluded edges
        self.parent = parent  # Parent node (used for reconstruction)

    def add_included_edge(self, edge):
        self.included_set.add(edge)
        self.included_list.append(edge)

    def __lt__(self, other):
        """
        Define the comparison operator for heapq to compare nodes based on their bound.
        This allows nodes to be ordered by their lower bound.
        """
        return self.bound < other.bound




def reduce_matrix(edges: list[list[float]]):

    reduced_matrix = [row[:] for row in edges]
    reduced_cost = 0
    for edge in range(len(reduced_matrix)):
        min_cost = math.inf
        for cost in range(len(reduced_matrix)):
            min_cost = min(reduced_matrix[edge][cost], min_cost)

        if min_cost != math.inf and min_cost > 0:
            reduced_cost += min_cost
            for cost in range(len(reduced_matrix)):
                if reduced_matrix[edge][cost] != math.inf:
                    reduced_matrix[edge][cost] -= min_cost

    for cost in range(len(reduced_matrix)):
        min_cost = math.inf
        for edge in range(len(reduced_matrix)):
            min_cost = min(reduced_matrix[edge][cost], min_cost)

        if min_cost != math.inf and min_cost > 0:
            reduced_cost += min_cost
            for edge in range(len(reduced_matrix)):
                if reduced_matrix[edge][cost] != math.inf:
                    reduced_matrix[edge][cost] -= min_cost

    return reduced_matrix, reduced_cost



def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []
