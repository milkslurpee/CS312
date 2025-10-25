# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point
import time

def compute_hull_other(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    return []


def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    sorted_points = sorted(points, key=lambda point: point[0])  # sorted() used Timsort which is O(nlogn)
    start_time = time.time()
    convex_hull = divide_and_conquer(sorted_points)  # By the Master Theorem, T(n) = 2T(n/2) + O(n) → O(nlogn)
    end_time = time.time()

    print(f'Time Elapsed (Convex Hull): {end_time - start_time:.3f} sec')
    return convex_hull


def divide_and_conquer(
        points):  # divide and conquer recurses down logn times and considered every point on its way back up, so it's O(nlogn)
    if len(points) < 3:  # base case
        return points

    mid = len(points) // 2  # Since the problem size is cut in half each time, we recurse down O(logn) times
    left_hull = divide_and_conquer(points[:mid])  # recursive calls
    right_hull = divide_and_conquer(points[mid:])

    return merge_hulls(left_hull, right_hull)  # worst case scenario of merge is that all points are along the hull and must be considered O(n)


def merge_hulls(left_hull, right_hull):  # Worst case: all points are on the boundary (L + R) = O(n),  so merging is O(n)

    left_start = max(left_hull, key=lambda p: p[0])
    right_start = min(right_hull, key=lambda p: p[0])

    upper = find_upper_tangent(left_hull, right_hull, left_start,
                               right_start)  # iterates through points along the hull of both the left and right hulls: O(L + R)
    lower = find_lower_tangent(left_hull, right_hull, left_start,
                               right_start)  # iterates through points along the hull of both the left and right hulls: O(L + R)

    return construct_hull(left_hull, right_hull, upper, lower)


def find_upper_tangent(left_hull, right_hull, left_start, right_start):
    i, j = left_hull.index(left_start), right_hull.index(right_start)
    left, right = True, True

    while left or right:  # iterates through points along the hull of both the left and right hulls: O(L + R)
        left, right = False, False
        while True:
            prev_i = (i - 1) % len(left_hull)
            new_slope = (right_hull[j][1] - left_hull[prev_i][1]) / (right_hull[j][0] - left_hull[prev_i][0])
            old_slope = (right_hull[j][1] - left_hull[i][1]) / (right_hull[j][0] - left_hull[i][0])
            if new_slope < old_slope:
                left = True
                i = prev_i
            else:
                break
        while True:
            next_j = (j + 1) % len(right_hull)
            new_slope = (right_hull[next_j][1] - left_hull[i][1]) / (right_hull[next_j][0] - left_hull[i][0])
            old_slope = (right_hull[j][1] - left_hull[i][1]) / (right_hull[j][0] - left_hull[i][0])
            if new_slope > old_slope:
                right = True
                j = next_j
            else:
                break
    return i, j


def find_lower_tangent(left_hull, right_hull, left_start, right_start):
    i, j = left_hull.index(left_start), right_hull.index(right_start)
    left, right = True, True

    while left or right:  # iterates through points along the hull of both the left and right hulls: O(L + R)
        left, right = False, False
        while True:
            next_i = (i + 1) % len(left_hull)
            new_slope = (right_hull[j][1] - left_hull[next_i][1]) / (right_hull[j][0] - left_hull[next_i][0])
            old_slope = (right_hull[j][1] - left_hull[i][1]) / (right_hull[j][0] - left_hull[i][0])
            if new_slope > old_slope:
                left = True
                i = next_i
            else:
                break
        while True:
            prev_j = (j - 1) % len(right_hull)
            new_slope = (right_hull[prev_j][1] - left_hull[i][1]) / (right_hull[prev_j][0] - left_hull[i][0])
            old_slope = (right_hull[j][1] - left_hull[i][1]) / (right_hull[j][0] - left_hull[i][0])
            if new_slope < old_slope:
                right = True
                j = prev_j
            else:
                break
    return i, j


def construct_hull(left_hull, right_hull, upper,
                   lower):  # iterates through points along the hull of both the left and right hulls: O(L + R)
    final_hull = []

    i = lower[0]
    while i != upper[0]:  # Traverse left hull from lower to upper tangent → O(L)
        final_hull.append(left_hull[i])
        i = (i + 1) % len(left_hull)
    final_hull.append(left_hull[upper[0]])

    j = upper[1]
    while j != lower[1]:  # Traverse right hull from upper to lower tangent → O(R)
        final_hull.append(right_hull[j])
        j = (j + 1) % len(right_hull)
    final_hull.append(right_hull[lower[1]])

    return final_hull
