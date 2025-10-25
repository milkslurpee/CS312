# Project Report - Convex Hull

## Baseline

### Design Discussion

I did my project with my brother Luke. 

#### Discussion Points
- We start by sorting the plot of points by their x values
- Then we start our divide and conquer algorithm by recursively dividing the plot into subplots
- The base case is a plot of 2 points, where we "compute the convex hull" by connecting the two points 
- As we recurse back up we merge the two hulls
  - find the common upper and lower tangents of the two hulls and draw a line between them
  - get rid of inside lines from the two hulls
- That should leave us with a finished convex hull.
### Theoretical Analysis - Convex Hull Divide-and-Conquer

#### Time 

```pycon
def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if len(points) < 3:
        return points
        
    sorted_points = sorted(points, key=lambda point: point[0]) # sorted() uses Timsort which is O(nlogn)

    start_time = time.time()
    polygon = divide_and_conquer(sorted_points)
    end_time = time.time()

    hull_points = [(p[0], p[1]) for p in polygon]
    print(f'Time Elapsed (Convex Hull): {end_time - start_time:.3f} sec')

    return hull_points

def divide_and_conquer(points):
    if len(points) < 3:
        return points

    mid = len(points) // 2                          #
    left_hull = divide_and_conquer(points[:mid])
    right_hull = divide_and_conquer(points[mid:])

    return merge_hulls(left_hull, right_hull)

def merge_hulls(left_hull, right_hull):
    left_start = max(left_hull, key=lambda p: p[0])
    right_start = min(right_hull, key=lambda p: p[0])

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

    while left or right:
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
```

#### Space

```pycon
def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if len(points) < 3:
        return points

    sorted_points = sorted(points, key=lambda point: point[0])

    start_time = time.time()
    polygon = divide_and_conquer(sorted_points)
    end_time = time.time()

    hull_points = [(p[0], p[1]) for p in polygon]
    print(f'Time Elapsed (Convex Hull): {end_time - start_time:.3f} sec')

    return hull_points

def divide_and_conquer(points):
    if len(points) < 3:
        return points

    mid = len(points) // 2
    left_hull = divide_and_conquer(points[:mid])
    right_hull = divide_and_conquer(points[mid:])

    return merge_hulls(left_hull, right_hull)

def merge_hulls(left_hull, right_hull):
    left_start = max(left_hull, key=lambda p: p[0])
    right_start = min(right_hull, key=lambda p: p[0])

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

    while left or right:
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
```

## Core

### Design Discussion

My core test passed along with my baseline tests.

### Empirical Data - Convex Hull Divide-and-Conquer

| N     | Time (sec) |
|-------| ---------- |
| 10    | 0.0003     |
| 100   | 0.0006     |
| 1000  | 0.0035     |
| 10000 | 0.0347     |
| 20000 | 0.0692     |
| 40000 | 0.1397     |
| 50000 | 0.1845     |

### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: *copy from section above* 
- Empirical order of growth (if different from theoretical): 

![img](img.png)

*Fill me in*

## Stretch 1

### Design Discussion

*Fill me in*

### Chosen Convex Hull Implementation Description

*Fill me in*

### Empirical Data

| N     | time (ms) |
|-------|-----------|
| 10    |           |
| 100   |           |
| 1000  |           |
| 10000 |           |
| 20000 |           |
| 40000 |           |
| 50000 |           |

### Comparison of Chosen Algorithm with Divide-and-Conquer Convex Hull

#### Algorithmic Differences

*Fill me in*

#### Performance Differences

*Fill me in*

## Stretch 2

*Fill me in*

## Project Review

*Fill me in*

