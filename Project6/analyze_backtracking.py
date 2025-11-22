import random
from pprint import pprint
from time import time
from typing import Callable

from tsp_solve_backtracking import greedy_tour
from tsp_solve_backtracking import backtracking
from utils import Timer
from utils import generate_network   # your function to generate edges


def run_solver(edges, solver: Callable):
    """Run a TSP solver and return only the runtime."""
    timer = Timer(10_000)   # very large; we measure actual wall-clock separately
    start = time()
    solver(edges, timer)
    return time() - start


def generate_and_analyze(seed: int, n: int, solver: Callable) -> tuple[int, float]:
    """Generate random TSP instance, run solver, return runtime."""
    random.seed(seed)

    # generate edges only; discard locations
    _, edges = generate_network(
        n,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=seed,
    )

    runtime = run_solver(edges, solver)
    return n, runtime


def _compute_average_runtimes(runtimes):
    groups = {}
    for n, runtime in runtimes:
        groups.setdefault(n, []).append(runtime)

    ave_runtimes = []
    for size, times in sorted(groups.items()):
        if len(times) > 2:
            times = sorted(times)[1:-1]  # drop min and max
        ave_runtimes.append((size, round(sum(times) / len(times), 4)))
    return ave_runtimes


def _print_markdown_table(ave_runtimes, headers):
    header_widths = [len(h) for h in headers]

    rows = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("-" * len(h) for h in headers) + " |"
    ]

    for row in ave_runtimes:
        formatted = "| " + " | ".join(
            f"{str(field):<{width}}"
            for field, width in zip(row, header_widths)
        ) + " |"
        rows.append(formatted)

    print("Copy this markdown table into your report:\n")
    print("\n".join(rows))


def analyze(solver_name: str):
    if solver_name == "greedy":
        solver = greedy_tour
    elif solver_name == "backtracking":
        solver = backtracking
    else:
        raise ValueError("solver_name must be 'greedy' or 'backtracking'")

    sizes = [5, 10, 12, 14, 16, 20, 25]  # backtracking can’t handle large n
    iterations = 5

    runtimes = []

    print(f"Running TSP runtime analysis for {solver_name}...\n")

    # warmup
    print("Warm-up...")
    _, edges = generate_network(5, True, 0.2, False, 0)
    run_solver(edges, solver)
    print("Warm-up complete.\n")

    for n in sizes:
        print(f"Testing {n} cities...")
        for i in range(iterations):
            seed = 100 + i
            size, runtime = generate_and_analyze(seed, n, solver)
            runtimes.append((size, runtime*1000))

    ave_runtimes = _compute_average_runtimes(runtimes)

    print()
    _print_markdown_table(ave_runtimes, ["N", "Time (sec)"])

    # save raw data
    filename = f"_runtimes.py"
    with open(filename, "w") as f:
        print("runtimes = ", end="", file=f)
        pprint(runtimes, f)

    print(f"\n{filename} written successfully.\n")


if __name__ == "__main__":
    analyze("greedy")         # or analyze("backtracking")