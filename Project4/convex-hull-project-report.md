# Project Report - Convex Hull

## Baseline

### Design Discussion

I did my project with my brother Luke. 

#### Discussion Points
- We start by sorting the points by their x values
- Then we recursively divide the plot into subplots
- The base case is a plot of 2 points, we compute the convex hull; we connect the two points 
- As we recurse back up we merge the two hulls
  - find the common upper and lower tangents of the two hulls and draw a line between them
  - get rid of inside lines from the two hulls
- We think that's about it. It should leave us with a finished convex hull.
### Theoretical Analysis - Convex Hull Divide-and-Conquer

#### Time 

*Fill me in*

#### Space

*Fill me in*

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

