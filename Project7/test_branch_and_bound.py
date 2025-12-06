# ---------------------------------- Imports --------------------------------- #
from byu_pytest_utils import tier

from tsp_core import Timer, generate_network, score_tour
from tsp_solve import greedy_tour, branch_and_bound, branch_and_bound_smart, \
    PARAMS_FOR_SMART_BRANCH_AND_BOUND_SMART_TEST
from tsp_test_utils import assert_valid_tours


from copy import deepcopy
import math
# -------------------------------- Test tiers -------------------------------- #
core = tier('core', 0)
stretch2 = tier('stretch2', 1)

# -------------------------------- Core tests -------------------------------- #
# TODO - do we need a better core test, or is this a good assessment of whether they did B&B correctly?

def test_branch_and_bound():
    """
    Test the branch_and_bound function.

    - Ensure that the algorithm runs correctly, terminates within time limit, and returns the best tour.
    - Verify that the solution found is valid and has the correct score.
    """

    # Test data: a simple 4-city TSP problem with known distances
    edges = [
        [math.inf, 10, 15, 20],
        [10, math.inf, 35, 25],
        [15, 35, math.inf, 30],
        [20, 25, 30, math.inf]
    ]

    # Initialize a Timer with a 10-second time limit
    timer = Timer(time_limit=10)

    # Run Branch and Bound algorithm
    stats = branch_and_bound(edges, timer)

    # Ensure the algorithm did not time out
    assert not timer.time_out(), "The algorithm timed out!"

    # Ensure the returned solution is valid (i.e., the tour should visit all cities once)
    tour = stats[0].tour
    assert len(tour) == len(edges), "The tour length is incorrect!"

    # Ensure the tour is valid (no repeated cities)
    assert len(set(tour)) == len(tour), "The tour contains repeated cities!"

    # Calculate the score of the returned tour and compare with the expected score
    calculated_score = score_tour(tour, edges)
    expected_score = 80  # This should be the known optimal solution for this small problem

    # Check if the calculated score is equal to the expected score
    assert calculated_score == expected_score, f"Expected score: {expected_score}, but got: {calculated_score}"

    # Check that the solution statistics are correct
    assert stats[0].n_nodes_expanded > 0, "No nodes were expanded!"
    assert stats[0].n_nodes_pruned >= 0, "Negative nodes pruned!"
    assert stats[0].score == expected_score, f"Expected score: {expected_score}, but got: {stats[0].score}"

    print("Branch and Bound test passed!")


# Call the test
test_branch_and_bound()


# @core
# def test_branch_and_bound():
#     """
#     - Greedy should run almost instantly.
#     - B&B should search the entire space in less than 3 minutes.
#       (A good implementation should finish in seconds).
#     - B&B should find a better score than greedy (on this graph).
#     """

#     locations, edges = generate_network(
#         15,
#         euclidean=True,
#         reduction=0.2,
#         normal=False,
#         seed=312,
#     )

#     timer = Timer(5)
#     greedy_stats = greedy_tour(deepcopy(edges), timer)
#     assert not timer.time_out()
#     assert_valid_tours(edges, greedy_stats)
#     greedy_score = score_tour(greedy_stats[-1].tour, edges)

#     timer = Timer(120)
#     stats = branch_and_bound(deepcopy(edges), timer)
#     assert not timer.time_out()
#     assert_valid_tours(edges, stats)
#     bnb_score = score_tour(stats[-1].tour, edges)

#     assert bnb_score < greedy_score


# ------------------------------ Stretch 2 tests ----------------------------- #
@stretch2
def test_branch_and_bound_smart():
    """
    Your Smart B&B algorithm should find a better answer
    than your B&B algorithm in the same amount of time.
    """
    timeout = PARAMS_FOR_SMART_BRANCH_AND_BOUND_SMART_TEST.pop('timeout')
    locations, edges = generate_network(
        **PARAMS_FOR_SMART_BRANCH_AND_BOUND_SMART_TEST
    )

    timer = Timer(timeout)
    bnb_stats = branch_and_bound(deepcopy(edges), timer)
    assert_valid_tours(edges, bnb_stats)
    bnb_score = score_tour(bnb_stats[-1].tour, edges)

    timer = Timer(timeout)
    stats = branch_and_bound_smart(deepcopy(edges), timer)
    assert_valid_tours(edges, stats)
    smart_score = score_tour(stats[-1].tour, edges)

    assert smart_score < bnb_score
