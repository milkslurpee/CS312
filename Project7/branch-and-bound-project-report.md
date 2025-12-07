# Project Report - Branch and Bound

## Baseline

### Design Experience

I did my design experience with Luke my little brother

For the matrix reduction we need to start by:
- iterating through each node (row reduction)
- for each node, find the minimum cost edge and subtract it from the other edge values
- Add all the minimum costs together as the initial cost
- Do this^ all again but column-wise, continuously adding them to the initial cost
- Return the reduced matrix, and the initial cost

### Theoretical Analysis - Reduced Cost Matrix

#### Time 

```pycon
def reduce_matrix(edges: list[list[float]]):                #O(n^2 + 2n(2n)) -> O(n^2)

    reduced_matrix = [row[:] for row in edges]              #O(n^2) make a copy of the matrix which is n by n
    reduced_cost = 0
    for edge in range(len(reduced_matrix)):                 #O(n) iterate through all nodes, not "edges". I coded this late last night and it made sense at the time lol. 
        min_cost = math.inf
        for cost in range(len(reduced_matrix)):                 #O(n) iterate through all edges, finding minimum cost
            min_cost = min(reduced_matrix[edge][cost], min_cost)

        if min_cost != math.inf and min_cost > 0:
            reduced_cost += min_cost
            for cost in range(len(reduced_matrix)):             #O(n) iterate again to update distances
                if reduced_matrix[edge][cost] != math.inf:
                    reduced_matrix[edge][cost] -= min_cost

    for cost in range(len(reduced_matrix)):                 #O(n) iterating through nodes column-wise. Again, sorry my names don't make sense. I was really tired.
        min_cost = math.inf
        for edge in range(len(reduced_matrix)):                 #O(n) iterate through edges
            min_cost = min(reduced_matrix[edge][cost], min_cost)

        if min_cost != math.inf and min_cost > 0:
            reduced_cost += min_cost
            for edge in range(len(reduced_matrix)):             
                if reduced_matrix[edge][cost] != math.inf:
                    reduced_matrix[edge][cost] -= min_cost

    return reduced_matrix, reduced_cost


```

The Time Complexity is O(n^2 + 2n(2n)) or just **O(n^2)**. This is because for both the row reduction and column reduction we first iterate through all the nodes, and then we iterate through all the edges to find the minimum value. We then iterate through again to update the matrix values with the reduced values. Ultimately though, everything is just dominated by O(n^2).


#### Space

```pycon
def reduce_matrix(edges: list[list[float]]):

    reduced_matrix = [row[:] for row in edges]          #O(n^2) creating copy of original n by n matrix. 
    reduced_cost = 0                                    #O(1)
    for edge in range(len(reduced_matrix)):
        min_cost = math.inf                             #O(1)
        for cost in range(len(reduced_matrix)):
            min_cost = min(reduced_matrix[edge][cost], min_cost)       

        if min_cost != math.inf and min_cost > 0:
            reduced_cost += min_cost
            for cost in range(len(reduced_matrix)):
                if reduced_matrix[edge][cost] != math.inf:
                    reduced_matrix[edge][cost] -= min_cost

    for cost in range(len(reduced_matrix)):
        min_cost = math.inf                         #O(1)
        for edge in range(len(reduced_matrix)):
            min_cost = min(reduced_matrix[edge][cost], min_cost)

        if min_cost != math.inf and min_cost > 0:
            reduced_cost += min_cost
            for edge in range(len(reduced_matrix)):
                if reduced_matrix[edge][cost] != math.inf:
                    reduced_matrix[edge][cost] -= min_cost

    return reduced_matrix, reduced_cost


```

The space complexity is **O(n^2)** solely due to the fact that we made a copy of the n by n matrix. I probably could have made a version that mutates the orignal matrix, but I assumed that could cause problems for core (which I couldn't finish in time).

## Core

### Design Experience

*Fill me in*

### Theoretical Analysis - Branch and Bound TSP

#### Time 

*Fill me in*

#### Space

*Fill me in*

### Empirical Data

| N   | Seed | Solution | time (ms) |
|-----|------|----------|-----------|
| 5   |      |          |           |
| 10  |      |          |           |
| 15  |      |          |           |
| 20  |      |          |           |
| 30  |      |          |           |
| 50  |      |          |           |

### Comparison of Theoretical and Empirical Results

- Empirical order of growth: 
- Measured constant of proportionality: 

![img](img.png)

*Fill me in*

## Stretch 1 

### Design Experience

*Fill me in*

### Search Space Over Time

![Plot demonstrating search space explored over time]()

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*

### Selected PQ Key

*Fill me in*

### Branch and Bound versus Smart Branch and Bound

*Fill me in*

## Project Report 

I spent about 5 hours on core, and just got really stuck. I'm not super happy I couldn't get it done, considering Baseline was actually super easy and only took me a couple hours.
Other than that the project went fine lol. I did my project report with Luke my little brother.

Luke and I largely coded the reduce_matrix function the same. We did have some differences. Most were trivial, like different methods of copying the matrix, and finding minimum cost edges. The only difference that may be nontrivial is that I skipped infinite values when updating the matrix rows and columns, and Luke didn't. This doesn't change anything since infinity - anything is still infinity, but mine may run a bit faster since I'm skipping some computations.

