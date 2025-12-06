import math
import random

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





    return []


def reduce_matrix(edges: list[list[float]]):

    reduced_cost = 0
    for edge in range(len(edges)):
        min_cost = math.inf
        for cost in range(len(edges)):
            min_cost = min(edges[edge][cost], min_cost)

        if min_cost != math.inf and min_cost > 0:
            reduced_cost += min_cost
            for cost in range(len(edges)):
                if edges[edge][cost] != math.inf:
                    edges[edge][cost] -= min_cost

    for cost in range(len(edges)):
        min_cost = math.inf
        for edge in range(len(edges)):
            min_cost = min(edges[edge][cost], min_cost)

        if min_cost != math.inf and min_cost > 0:
            reduced_cost += min_cost
            for edge in range(len(edges)):
                if edges[edge][cost] != math.inf:
                    edges[edge][cost] -= min_cost

    return edges, reduced_cost



def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []
