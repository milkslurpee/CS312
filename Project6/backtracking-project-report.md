# Project Report - Backtracking

## Baseline

### Design Experience

I did my design experience with my brother Luke
- For baseline we are going to run a for loop to loop through all the cities; These will be the starting points.
- From each starting city, we will continuously pick the nearest city until we either find a solution, reach a dead end, or the timer runs out
- After finding our first solution, we will kill any paths that have a greater cost than that solution. If we find a cheaper solution, then we will append that solution to the list of solutions.
- After iterating through all the cities, we will return all of the solutions that we have found.

### Theoretical Analysis - Greedy

#### Time 

*Fill me in*

#### Space

*Fill me in*

### Empirical Data - Greedy

| N   | reduction | time (ms) |
|-----|-----------|-----------|
| 5   | 0         |           |
| 10  | 0         |           |
| 15  | 0         |           |
| 20  | 0         |           |
| 25  | 0         |           |
| 30  | 0         |           |
| 35  | 0         |           |
| 40  | 0         |           |
| 45  | 0         |           |
| 50  | 0         |           |

### Comparison of Theoretical and Empirical Results - Greedy

- Theoretical order of growth: 
- Empirical order of growth (if different from theoretical):

## Core

### Design Experience

I did my design experience with Luke
- We will start by putting the starting city on the stack
- Then we'll start the loop that runs while the stack isn't empty and the timer hasnt run out
- In the loop we pop the path (the starting city on first iteration) and expand all children paths that haven't already been expanded
- If there is no solution, push that path back onto the stack
- If there is a solution AND it's the new cheapest solution, then add it to the list of solutions
- Return the list of solutions

### Theoretical Analysis - Backtracking

#### Time 

*Fill me in*

#### Space

*Fill me in*

### Empirical Data - Backtracking

| N   | reduction | time (ms) |
|-----|-----------|-----------|
| 5   | 0         |           |
| 10  | 0         |           |
| 15  | 0         |           |
| 20  | 0         |           |
| 25  | 0         |           |
| 30  | 0         |           |
| 35  | 0         |           |
| 40  | 0         |           |
| 45  | 0         |           |
| 50  | 0         |           |

### Comparison of Theoretical and Empirical Results - Backtracking

- Theoretical order of growth: 
- Empirical order of growth (if different from theoretical): 

### Greedy v Backtracking

*Fill me in*

### Water Bottle Scenario 

#### Scenario 1

**Algorithm:** 

*Fill me in*

#### Scenario 2

**Algorithm:** 

*Fill me in*

#### Scenario 2

**Algorithm:** 

*Fill me in*


## Stretch 1

### Design Experience

*Fill me in*

### Demonstrate BSSF Backtracking Works Better than No-BSSF Backtracking 

*Fill me in*

### BSSF Backtracking v Backtracking Complexity Differences

*Fill me in*

### Time v Solution Cost

![Plot]()

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*

### Cut Tree

*Fill me in*

### Plots 

*Fill me in*

## Project Review

*Fill me in*
