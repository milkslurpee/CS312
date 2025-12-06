import math

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


# Test matrix
test_matrix = [
    [math.inf, 34, 56, 12, 78, 45, 23, 67, 89, 43, 21, 54],
    [23, math.inf, 41, 89, 33, 54, 76, 12, 45, 67, 34, 22],
    [45, 67, math.inf, 32, 88, 19, 41, 53, 76, 29, 47, 38],
    [12, 89, 34, math.inf, 56, 77, 32, 44, 61, 53, 28, 49],
    [78, 33, 88, 56, math.inf, 45, 67, 89, 34, 76, 52, 63],
    [54, 76, 19, 77, 45, math.inf, 23, 55, 82, 38, 41, 27],
    [23, 41, 67, 32, 67, 23, math.inf, 34, 59, 46, 38, 52],
    [67, 12, 53, 44, 89, 55, 34, math.inf, 47, 61, 29, 43],
    [89, 45, 76, 61, 34, 82, 59, 47, math.inf, 28, 54, 37],
    [43, 67, 29, 53, 76, 38, 46, 61, 28, math.inf, 32, 45],
    [21, 34, 47, 28, 52, 41, 38, 29, 54, 32, math.inf, 26],
    [54, 22, 38, 49, 63, 27, 52, 43, 37, 45, 26, math.inf]
]

reduced_matrix, cost = reduce_matrix([row[:] for row in test_matrix])  # Make a copy
print(f"Reduction cost: {cost}")
print("Reduced matrix:")
for row in reduced_matrix:
    print([f"{x:5.1f}" if x != math.inf else "  inf" for x in row])