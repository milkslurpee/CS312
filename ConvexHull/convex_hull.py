import time
from PyQt5.QtCore import QPointF
from plotting import draw_hull

PAUSE = 0.5

def showHull(polygon, color):
    draw_hull(polygon, color)
    time.sleep(PAUSE)

def showText(text):
    print(text)

def compute_hull(points):
    if len(points) < 3:
        return points

    points = [QPointF(x, y) for x, y in points]
    sorted_points = sorted(points, key=lambda point: point.x())

    start_time = time.time()
    polygon = divide_and_conquer(sorted_points)
    end_time = time.time()

    hull_points = [(p.x(), p.y()) for p in polygon]
    draw_hull(hull_points, c="red")
    showText(f'Time Elapsed (Convex Hull): {end_time - start_time:.3f} sec')

    return hull_points

def divide_and_conquer(points):
    if len(points) < 3:
        return points

    mid = len(points) // 2
    left_hull = divide_and_conquer(points[:mid])
    right_hull = divide_and_conquer(points[mid:])

    return merge_hulls(left_hull, right_hull)

def merge_hulls(left_hull, right_hull):
    left_start = max(left_hull, key=lambda p: p.x())
    right_start = min(right_hull, key=lambda p: p.x())

    upper = find_upper_tangent(left_hull, right_hull, left_start, right_start)
    lower = find_lower_tangent(left_hull, right_hull, left_start, right_start)

    return construct_hull(left_hull, right_hull, upper, lower)

def find_upper_tangent(left_hull, right_hull, left_start, right_start):
    i, j = left_hull.index(left_start), right_hull.index(right_start)
    left, right = True, True

    while left or right:
        left, right = False, False

        while True:
            prev_i = (i - 1) % len(left_hull)
            new_slope = (right_hull[j].y() - left_hull[prev_i].y()) / (right_hull[j].x() - left_hull[prev_i].x())
            old_slope = (right_hull[j].y() - left_hull[i].y()) / (right_hull[j].x() - left_hull[i].x())
            if new_slope < old_slope:
                left = True
                i = prev_i
            else:
                break

        while True:
            next_j = (j + 1) % len(right_hull)
            new_slope = (right_hull[next_j].y() - left_hull[i].y()) / (right_hull[next_j].x() - left_hull[i].x())
            old_slope = (right_hull[j].y() - left_hull[i].y()) / (right_hull[j].x() - left_hull[i].x())
            if new_slope > old_slope:
                right = True
                j = next_j
            else:
                break

    return i, j

def find_lower_tangent(left_hull, right_hull, left_start, right_start):
    i, j = left_hull.index(left_start), right_hull.index(right_start)
    left, right = True, True

    while left or right:
        left, right = False, False

        while True:
            next_i = (i + 1) % len(left_hull)
            new_slope = (right_hull[j].y() - left_hull[next_i].y()) / (right_hull[j].x() - left_hull[next_i].x())
            old_slope = (right_hull[j].y() - left_hull[i].y()) / (right_hull[j].x() - left_hull[i].x())
            if new_slope > old_slope:
                left = True
                i = next_i
            else:
                break

        while True:
            prev_j = (j - 1) % len(right_hull)
            new_slope = (right_hull[prev_j].y() - left_hull[i].y()) / (right_hull[prev_j].x() - left_hull[i].x())
            old_slope = (right_hull[j].y() - left_hull[i].y()) / (right_hull[j].x() - left_hull[i].x())
            if new_slope < old_slope:
                right = True
                j = prev_j
            else:
                break

    return i, j

def construct_hull(left_hull, right_hull, upper, lower):
    final_hull = []
    i = lower[0]

    while i != upper[0]:
        final_hull.append(left_hull[i])
        i = (i + 1) % len(left_hull)
    final_hull.append(left_hull[upper[0]])

    j = upper[1]
    while j != lower[1]:
        final_hull.append(right_hull[j])
        j = (j + 1) % len(right_hull)
    final_hull.append(right_hull[lower[1]])

    return final_hull
