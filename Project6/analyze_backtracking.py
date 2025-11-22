import random
from pprint import pprint
from time import time
from typing import Callable

from tsp_solve_backtracking import greedy_tour, backtracking
from utils import Timer, generate_network


def run_solver(edges, solver: Callable):
    timer = Timer(60)  # 60 second timeout
    start = time()
    result = solver(edges, timer)
    runtime = time() - start

    # Check if we got a valid solution (not just timeout)
    valid_solution = result and len(result) > 0 and result[0].score < float('inf')
    return runtime, valid_solution


def generate_and_analyze(seed: int, n: int, reduction: float, solver: Callable) -> tuple[int, float, float, bool]:
    """Generate random TSP instance, run solver, return runtime and success status."""
    random.seed(seed)
    _, edges = generate_network(
        n,
        euclidean=True,
        reduction=reduction,
        normal=False,
        seed=seed
    )
    runtime, valid_solution = run_solver(edges, solver)
    return n, reduction, runtime, valid_solution


def _compute_average_runtimes(runtimes):
    groups = {}
    for n, reduction, runtime, valid in runtimes:
        if valid:  # Only include successful runs
            groups.setdefault((n, reduction), []).append(runtime)

    ave_runtimes = []
    for (size, reduction), times in sorted(groups.items()):
        if not times:  # Skip if no valid runs
            continue
        if len(times) > 2:
            times = sorted(times)[1:-1]  # drop min and max
        ave_runtimes.append((size, reduction, round(sum(times) / len(times) * 1000, 2)))  # ms
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
    solver = greedy_tour if solver_name == "greedy" else backtracking

    # Use much smaller sizes for backtracking
    if solver_name == "backtracking":
        sizes = [5, 10, 15, 20]  # Backtracking can't handle large n
        print("Using smaller sizes for backtracking due to O(n!) complexity")
    else:
        sizes = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

    reductions = [0.0]
    iterations = 3  # Reduce iterations for backtracking

    runtimes = []
    timeout_count = 0
    should_stop = False  # Flag to stop testing larger sizes

    print(f"Starting analysis for {solver_name}...")
    print(f"Sizes: {sizes}")
    print(f"Iterations: {iterations}")

    # Warm-up with smallest size
    print("Warm-up...")
    _, edges = generate_network(5, True, 0, False, 0)
    run_solver(edges, solver)
    print("Warm-up complete.\n")

    for n in sizes:
        if should_stop:
            print(f"\nSTOPPING EARLY: Previous size hit 60s timeout. Skipping n={n} and all larger sizes.")
            break

        print(f"\nTesting n={n}...")
        size_timeouts = 0

        for i in range(iterations):
            if should_stop:
                break

            print(f"  Iteration {i + 1}/{iterations}", end="")
            seed = 100 + i
            n_val, red_val, runtime, valid = generate_and_analyze(seed, n, reductions[0], solver)

            if runtime >= 60.0:  # HARD STOP at 60 seconds
                print(f" - {runtime:.2f}s - TIMEOUT! STOPPING HERE.")
                timeout_count += 1
                size_timeouts += 1
                should_stop = True
                break
            elif valid:
                # Only store the data we want in the final table
                runtimes.append((n_val, red_val, runtime))
                print(f" - {runtime:.2f}s - VALID")
            else:
                print(f" - {runtime:.2f}s - INVALID")
                timeout_count += 1
                size_timeouts += 1

        if size_timeouts == iterations and not should_stop:
            print(f"  WARNING: All iterations for n={n} produced invalid solutions")
            # Only stop if we actually hit 60s timeout, not just invalid solutions

    print(f"\nCompleted {solver_name} analysis.")
    print(f"Total timeouts: {timeout_count}")

    # Only compute averages for sizes with valid data
    ave_runtimes = _compute_average_runtimes_clean(runtimes)

    if ave_runtimes:
        _print_markdown_table(ave_runtimes, ["N", "reduction", "time (ms)"])

        # Save raw data
        filename = f"{solver_name}_runtimes.py"
        with open(filename, "w") as f:
            print("runtimes = ", end="", file=f)
            pprint(runtimes, f)
        print(f"\n{filename} written successfully.")
    else:
        print("No valid data collected - all runs timed out or produced invalid solutions")


def _compute_average_runtimes_clean(runtimes):
    """Modified version that works with clean runtime data (no boolean values)"""
    groups = {}
    for n, reduction, runtime in runtimes:
        groups.setdefault((n, reduction), []).append(runtime)

    ave_runtimes = []
    for (size, reduction), times in sorted(groups.items()):
        if not times:  # Skip if no valid runs
            continue
        if len(times) > 2:
            times = sorted(times)[1:-1]  # drop min and max
        ave_runtimes.append((size, reduction, round(sum(times) / len(times) * 1000, 2)))  # ms
    return ave_runtimes


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        algorithm = sys.argv[1]
    else:
        algorithm = "backtracking"

    print(f"Running analysis for: {algorithm}")
    analyze(algorithm)