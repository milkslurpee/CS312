import random
from pprint import pprint
from time import time
from typing import Callable

from main import generate_random_points
from convex_hull import compute_hull_dvcq


def generate_and_analyze_points(seed: int, n: int, analyze: Callable) -> tuple[int, float]:
    """Generate uniform random points, run convex hull, return runtime in seconds."""
    random.seed(seed)
    points = generate_random_points("uniform", n, seed)

    start = time()
    analyze(points)
    duration = time() - start

    return n, duration


def _compute_average_runtimes(runtimes):
    groups = {}
    for n, runtime in runtimes:
        groups.setdefault(n, []).append(runtime)

    ave_runtimes = []
    for size, times in sorted(groups.items()):
        if len(times) > 2:
            times = sorted(times)[1:-1]  # drop lowest and highest
        ave_runtimes.append((size, round(sum(times) / len(times), 4)))
    return ave_runtimes


def _print_markdown_table(ave_runtimes, headers):
    header_widths = [len(header) for header in headers]

    rows = [
        '| ' + ' | '.join(headers) + ' |',
        '| ' + ' | '.join('-' * len(header) for header in headers) + ' |'
    ]

    for row in ave_runtimes:
        formatted = '| ' + ' | '.join(
            f'{str(field):<{width}}'
            for field, width in zip(row, header_widths)
        ) + ' |'
        rows.append(formatted)

    print('Copy this markdown table into your report:')
    print()
    print('\n'.join(rows))


def main():
    sizes = [10, 100, 1000, 10000, 20000, 40000, 50000]
    iterations = 5  # Number of runs per size to average runtime

    runtimes = []

    print('Running convex hull runtime analysis (uniform distribution only)...\n')

    # Warm-up run to avoid first-run overhead
    print("Performing warm-up run...")
    warmup_points = generate_random_points("uniform", 10, 0)
    compute_hull_dvcq(warmup_points)
    print("Warm-up complete.\n")

    for n in sizes:
        print(f'Testing {n} points...')
        for iteration in range(iterations):
            seed = 100 + iteration
            size, runtime = generate_and_analyze_points(seed, n, compute_hull_dvcq)
            runtimes.append((size, runtime))

    ave_runtimes = _compute_average_runtimes(runtimes)

    print()
    _print_markdown_table(ave_runtimes, ['N', 'Time (sec)'])

    # Save raw data to file
    filename = '_runtimes.py'
    with open(filename, 'w') as file:
        print('runtimes = ', end='', file=file)
        pprint(runtimes, file)

    print(f'\n{filename} written successfully.\n')



if __name__ == '__main__':
    main()
