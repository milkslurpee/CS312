import math
import random

from utils import Tour, SolutionStats, Timer, score_tour, Solver
from cuttree import CutTree


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



def backtracking(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []

def backtracking_bssf(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []

