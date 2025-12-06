# See additional instructions for these tests in the instructions for the project
import math
from tsp_solve import reduce_matrix

def test_reduced_cost_matrix_1():

    test_matrix = [                     # From HW4 Part2 Problem 1
        [math.inf, 7, 3, 12],
        [3, math.inf, 6, 14],
        [5, 8, math.inf, 6],
        [9, 3, 5, math.inf]
    ]
    expected_matrix = [
        [math.inf, 4, 0, 8],
        [0, math.inf, 3, 10],
        [0, 3, math.inf, 0],
        [6, 0, 2, math.inf]
    ]


    result, cost = reduce_matrix(test_matrix)

    if result == expected_matrix and cost == 15:
        pass
    else:
        raise Exception("Test failed")


def test_reduced_cost_matrix_2():

    test_matrix = [                 # made it up and reduced by hand
        [math.inf, 20, 30, 10],
        [15, math.inf, 60, 20],
        [25, 30, math.inf, 30],
        [10, 15, 20, math.inf]
    ]
    expected_matrix = [
        [math.inf, 5, 10, 0],
        [0, math.inf, 35, 5],
        [0, 0, math.inf, 5],
        [0, 0, 0, math.inf]
    ]

    result, cost = reduce_matrix(test_matrix)

    if result == expected_matrix and cost == 75:
        pass
    else:
        raise Exception("Test failed")

# Add more tests as necessary...
